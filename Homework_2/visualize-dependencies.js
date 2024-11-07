const https = require('https');
const fs = require('fs');
const { execSync } = require('child_process');

function getDependencies(filePath) {
    const content = fs.readFileSync(filePath, 'utf8');
    const packageJson = JSON.parse(content);
    return packageJson.dependencies || {};
}

function normalizeVersion(version) {
    const match = version.match(/(\d+\.\d+\.\d+)/); 
    return match ? match[0] : 'latest'; 
}

function fetchDependencies(pkg, version = 'latest') {
    return new Promise((resolve, reject) => {
        const url = `https://registry.npmjs.org/${pkg}/${version}`;
        
        https.get(url, (res) => {
            let data = '';

            res.on('data', (chunk) => {
                data += chunk;
            });

            res.on('end', () => {
                try {
                    const packageData = JSON.parse(data);
                    resolve(packageData.dependencies || {});
                } catch (error) {
                    reject(new Error(`Failed to parse response for ${pkg}@${version}: ${error.message}`));
                }
            });
        }).on('error', (err) => {
            reject(new Error(`Failed to fetch ${pkg}@${version}: ${err.message}`));
        });
    });
}

async function collectDependencies(dependencies, allDependencies = {}, visited = new Set()) {
    for (const [pkg, version] of Object.entries(dependencies)) {
        if (visited.has(pkg)) continue;
        visited.add(pkg);

        const normalizedVersion = normalizeVersion(version);

        try {
            const deps = await fetchDependencies(pkg, normalizedVersion);
            allDependencies[pkg] = Object.keys(deps);
            await collectDependencies(deps, allDependencies, visited);
        } catch (error) {
            console.error(error.message);
        }
    }
    return allDependencies;
}

function generateMermaidGraph(dependencies) {
    let graph = 'graph TD\n';
    for (const [pkg, deps] of Object.entries(dependencies)) {
        for (const dep of deps) {
            graph += `  ${pkg} --> ${dep}\n`;
        }
    }
    return graph;
}

function visualizeGraph(graph, outputPath, MermaidGraphPath) {
    fs.writeFileSync(MermaidGraphPath, graph);

    try {
        execSync(`mmdc -i ${MermaidGraphPath} -o ${outputPath}`, {
            stdio: ['ignore', 'ignore', 'ignore'], 
        });
    } catch (error) {
        console.error(`Failed to visualize graph: ${error.message}`);
    }
}

module.exports = {
    getDependencies,
    normalizeVersion,
    collectDependencies,
    generateMermaidGraph,
    visualizeGraph
};


if (require.main === module) {
    (async () => {
        try {
            const config = JSON.parse(fs.readFileSync('config.json', 'utf8'));

            const dependencies = getDependencies('package_dependecies.json');
            const allDependencies = await collectDependencies(dependencies);
            const graph = generateMermaidGraph(allDependencies);

            const MermaidGraphPath = 'Mermaid_graph.mmd'; 

            visualizeGraph(graph, config.output, MermaidGraphPath);

            console.log('Graph visualization completed successfully.');
        } catch (error) {
            console.error(`Error: ${error.message}`);
        }
    })();
}
