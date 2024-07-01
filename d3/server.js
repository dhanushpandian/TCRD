const express = require('express');
const neo4j = require('neo4j-driver');
const app = express();
const cors = require('cors');
const port = 3000;
app.use(cors()); 
const driver = neo4j.driver('bolt://localhost:7687', neo4j.auth.basic('neo4j', '12345678'));

app.get('/graph', async (req, res) => {
    let session; // Define session variable outside of try block
    try {
        session = driver.session(); // Initialize session
        const result = await session.run('MATCH (n)-[r]->(m) RETURN n, r, m LIMIT 100');

        const nodes = [];
        const relationships = [];

        result.records.forEach(record => {
            const node1 = record.get('n');
            const relationship = record.get('r');
            const node2 = record.get('m');

            nodes.push({
                id: node1.identity.low,
                label: node1.labels[0],
                properties: node1.properties
            });

            nodes.push({
                id: node2.identity.low,
                label: node2.labels[0],
                properties: node2.properties
            });

            relationships.push({
                id: relationship.identity.low,
                type: relationship.type,
                startNode: relationship.start.low,
                endNode: relationship.end.low,
                properties: relationship.properties
            });
        });

        // Deduplicate nodes
        const uniqueNodes = Array.from(new Set(nodes.map(node => node.id)))
            .map(id => nodes.find(node => node.id === id));

        res.json({ nodes: uniqueNodes, relationships });
    } catch (error) {
        console.error('Error fetching data from Neo4j:', error);
        res.status(500).send('Error fetching data from Neo4j');
    } finally {
        if (session) { // Check if session is defined
            await session.close(); // Close the session if it was created successfully
        }
    }
});

app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});
