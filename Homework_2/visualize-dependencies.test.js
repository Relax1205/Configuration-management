const fs = require('fs');
const path = require('path');
const {
    getDependencies,
    normalizeVersion,
    collectDependencies,
    generateMermaidGraph,
    visualizeGraph,
} = require('./visualize-dependencies');


function testGetDependencies() {
    const samplePackageJson = path.join(__dirname, 'sample_package.json');
    fs.writeFileSync(samplePackageJson, JSON.stringify({
        dependencies: {
            "express": "^4.17.1",
            "lodash": "^4.17.21"
        }
    }));

    const result = getDependencies(samplePackageJson);
    console.assert(JSON.stringify(result) === JSON.stringify({
        "express": "^4.17.1",
        "lodash": "^4.17.21"
    }), 'testGetDependencies failed');

    fs.unlinkSync(samplePackageJson); 
}


function testNormalizeVersion() {
    console.assert(normalizeVersion("1.2.3") === "1.2.3", 'testNormalizeVersion failed for valid version');
    console.assert(normalizeVersion("invalid") === "latest", 'testNormalizeVersion failed for invalid version');
}

function testGenerateMermaidGraph() {
    const dependencies = {
        "express": ["body-parser", "cookie-parser"],
        "lodash": []
    };
    const expectedGraph = `graph TD\n  express --> body-parser\n  express --> cookie-parser\n`;
    const resultGraph = generateMermaidGraph(dependencies);
    console.assert(resultGraph === expectedGraph, 'testGenerateMermaidGraph failed');
}

async function testCollectDependencies() {
    const dependencies = {
        "express": "^4.17.1",
        "lodash": "^4.17.21"
    };

    const originalFetchDependencies = global.fetchDependencies;
    global.fetchDependencies = async (pkg, version) => {
        if (pkg === "express") {
            return {
                "body-parser": "1.19.0",
                "cookie-parser": "1.4.5"
            };
        } else if (pkg === "lodash") {
            return {};
        }
        throw new Error(`Unexpected package: ${pkg}`);
    };

    const allDependencies = await collectDependencies(dependencies);
    
    console.assert(Object.keys(allDependencies).length > 0, 'testCollectDependencies failed');
    
    global.fetchDependencies = originalFetchDependencies;
}

async function runTests() {
    testGetDependencies();
    testNormalizeVersion();
    testGenerateMermaidGraph();
    await testCollectDependencies();
    console.log('All tests passed.');
}

runTests().catch(err => console.error(`Test failed: ${err.message}`));
