const { execSync } = require('child_process');
const fs = require('fs');
const AdmZip = require('adm-zip');

// Функция для извлечения файла package.json из архива
function extractPackageJson(archivePath) {
    const zip = new AdmZip(archivePath);
    const packageJsonEntry = zip.getEntry('package.json');

    if (!packageJsonEntry) {
        throw new Error('package.json not found in the archive');
    }

    const content = zip.readAsText(packageJsonEntry);
    return JSON.parse(content);
}

// Функция для получения зависимостей из package.json
function getDependencies(packageJson) {
    return packageJson.dependencies || {};
}

// Функция для нормализации версии (извлечение последней стабильной)
function normalizeVersion(version) {
    const match = version.match(/(\d+\.\d+\.\d+)/); // Ищем "x.y.z"
    return match ? match[0] : 'latest'; // Если нет точной версии, используем 'latest'
}

// Рекурсивная функция для сбора всех зависимостей
function collectDependencies(dependencies, allDependencies = {}, visited = new Set()) {
    for (const [pkg, version] of Object.entries(dependencies)) {
        if (visited.has(pkg)) continue;
        visited.add(pkg);

        const normalizedVersion = normalizeVersion(version);

        try {
            const result = execSync(`npm view ${pkg}@${normalizedVersion} dependencies --json`, {
                encoding: 'utf8',
                stdio: ['ignore', 'pipe', 'ignore'], 
            });

            if (!result) continue;

            const deps = JSON.parse(result);

            if (typeof deps !== 'object' || Array.isArray(deps) || !deps) {
                continue; // Пропускаем пакеты с некорректным форматом зависимостей
            }

            allDependencies[pkg] = Object.keys(deps);
            collectDependencies(deps, allDependencies, visited);
        } catch {
            // Игнорируем ошибки
        }
    }
    return allDependencies;
}

// Функция для генерации графа в формате Mermaid
function generateMermaidGraph(dependencies) {
    let graph = 'graph TD\n';
    for (const [pkg, deps] of Object.entries(dependencies)) {
        for (const dep of deps) {
            graph += `  ${pkg} --> ${dep}\n`;
        }
    }
    return graph;
}

// Функция для визуализации графа и сохранения его в файл
function visualizeGraph(graph, outputPath, MermaidGraphPath) {
    fs.writeFileSync(MermaidGraphPath, graph);

    try {
        execSync(`mmdc -i ${MermaidGraphPath} -o ${outputPath}`, {
            stdio: ['ignore', 'ignore', 'ignore'], // Подавляем все выходные потоки
        });
    } catch (error) {
        console.error(`Failed to visualize graph: ${error.message}`);
    }
}

module.exports = {
    extractPackageJson,
    getDependencies,
    normalizeVersion,
    collectDependencies,
    generateMermaidGraph,
    visualizeGraph
};

// Основная логика (выполняется только если скрипт запущен напрямую)
if (require.main === module) {
    (async () => {
        try {
            // Чтение конфигурации из файла
            const config = JSON.parse(fs.readFileSync('config.json', 'utf8'));

            const packageJson = extractPackageJson(config.archive);
            const dependencies = getDependencies(packageJson);
            const allDependencies = collectDependencies(dependencies);
            const graph = generateMermaidGraph(allDependencies);

            const MermaidGraphPath = 'Mermaid_graph.mmd'; 

            visualizeGraph(graph, config.output, MermaidGraphPath);

            console.log('Graph visualization completed successfully.');
        } catch (error) {
            console.error(`Error: ${error.message}`);
        }
    })();
}
