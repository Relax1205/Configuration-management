const { execSync } = require('child_process');
const fs = require('fs');
const AdmZip = require('adm-zip');
const {
    extractPackageJson,
    getDependencies,
    normalizeVersion,
    collectDependencies,
    generateMermaidGraph,
    visualizeGraph
} = require('./visualize-dependencies');

jest.mock('child_process');
jest.mock('fs');
jest.mock('adm-zip');

describe('Dependency Visualizer Functions', () => {
    beforeEach(() => {
        jest.clearAllMocks();
    });

    describe('extractPackageJson', () => {
        it('should extract and parse package.json from zip archive', () => {
            const mockContent = JSON.stringify({ dependencies: { lodash: '^4.17.21' } });
            const mockEntry = { name: 'package.json' };
            const mockZip = {
                getEntry: jest.fn().mockReturnValue(mockEntry),
                readAsText: jest.fn().mockReturnValue(mockContent)
            };

            AdmZip.mockImplementation(() => mockZip);

            const result = extractPackageJson('mock.zip');
            expect(result).toEqual(JSON.parse(mockContent));
        });

        it('should throw an error if package.json is not found', () => {
            const mockZip = { getEntry: jest.fn().mockReturnValue(null) };
            AdmZip.mockImplementation(() => mockZip);

            expect(() => extractPackageJson('mock.zip')).toThrow('package.json not found in the archive');
        });
    });

    describe('getDependencies', () => {
        it('should return dependencies from package.json', () => {
            const packageJson = { dependencies: { lodash: '^4.17.21' } };
            const result = getDependencies(packageJson);
            expect(result).toEqual(packageJson.dependencies);
        });

        it('should return an empty object if no dependencies exist', () => {
            const packageJson = {};
            const result = getDependencies(packageJson);
            expect(result).toEqual({});
        });
    });

    describe('normalizeVersion', () => {
        it('should return the normalized version', () => {
            expect(normalizeVersion('^4.17.21')).toBe('4.17.21');
        });

        it('should return "latest" if no valid version is found', () => {
            expect(normalizeVersion('some-invalid-version')).toBe('latest');
        });
    });

    function collectDependencies(dependencies) {
        const result = {};
        const visited = new Set();
    
        function visit(dep) {
            if (visited.has(dep)) return;
    
            visited.add(dep);
            const version = normalizeVersion(dependencies[dep]);
            const command = `npm view ${dep}@${version} dependencies --json`;
    
            try {
                const subDependencies = JSON.parse(execSync(command).toString());
                result[dep] = Object.keys(subDependencies);
                Object.keys(subDependencies).forEach(visit);
            } catch (error) {
                console.error(`Failed to collect dependencies for ${dep}: ${error.message}`);
                result[dep] = []; // Добавляем пустой массив для текущей зависимости
            }
        }
    
        Object.keys(dependencies).forEach(visit);
        return result;
    }
    

    describe('generateMermaidGraph', () => {
        it('should generate a mermaid graph representation of dependencies', () => {
            const dependencies = {
                express: ['lodash'],
                lodash: []
            };
            const graph = generateMermaidGraph(dependencies);
            expect(graph).toBe('graph TD\n  express --> lodash\n');
        });

        it('should return a graph with no dependencies', () => {
            const dependencies = {};
            const graph = generateMermaidGraph(dependencies);
            expect(graph).toBe('graph TD\n'); // Граф без зависимостей
        });
    });

    describe('visualizeGraph', () => {
        it('should visualize the graph and save it to a file', () => {
            const mockOutputPath = 'output.png';
            const mockGraph = 'graph TD\n  express --> lodash\n';
            const mockMermaidGraphPath = 'Mermaid_graph.mmd';

            visualizeGraph(mockGraph, mockOutputPath, mockMermaidGraphPath);
            expect(fs.writeFileSync).toHaveBeenCalledWith(mockMermaidGraphPath, mockGraph);
            expect(execSync).toHaveBeenCalledWith(`mmdc -i ${mockMermaidGraphPath} -o ${mockOutputPath}`, {
                stdio: ['ignore', 'ignore', 'ignore']
            });
        });

        it('should log an error if the visualization fails', () => {
            const mockGraph = 'graph TD\n  express --> lodash\n';
            const mockOutputPath = 'output.png';
            const mockMermaidGraphPath = 'Mermaid_graph.mmd';
            execSync.mockImplementation(() => { throw new Error('Visualization failed'); });

            console.error = jest.fn(); // Mock console.error

            visualizeGraph(mockGraph, mockOutputPath, mockMermaidGraphPath);
            expect(console.error).toHaveBeenCalledWith('Failed to visualize graph: Visualization failed');
        });
    });
});
