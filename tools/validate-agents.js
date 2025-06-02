// validate-agents.js
// Scans all agent.json files in agents/ and validates them against agent-manifest.schema.json
// Usage: node tools/validate-agents.js

const fs = require('fs');
const path = require('path');
const Ajv = require('ajv');
const addFormats = require('ajv-formats');

const agentsDir = path.join(__dirname, '../agents');
const schemaPath = path.join(__dirname, '../agent-manifest.schema.json');

// Load schema
const schema = JSON.parse(fs.readFileSync(schemaPath, 'utf-8'));
const ajv = new Ajv({ allErrors: true, allowUnionTypes: true });
addFormats(ajv); // Enable format validation (e.g., uri)
const validate = ajv.compile(schema);

let hasError = false;

function validateAgentManifest(agentPath) {
  const manifestPath = path.join(agentPath, 'agent.json');
  if (!fs.existsSync(manifestPath)) return;
  try {
    const manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf-8'));
    const valid = validate(manifest);
    if (!valid) {
      hasError = true;
      console.error(`❌ Validation failed for ${manifestPath}`);
      console.error('Validation errors:', JSON.stringify(validate.errors, null, 2));
    } else {
      console.log(`✅ ${manifestPath} is valid.`);
    }
  } catch (err) {
    hasError = true;
    console.error(`❌ Error processing ${manifestPath}`);
    console.error(err.stack || err);
  }
}

fs.readdirSync(agentsDir).forEach(agentFolder => {
  const agentPath = path.join(agentsDir, agentFolder);
  if (fs.statSync(agentPath).isDirectory()) {
    validateAgentManifest(agentPath);
  }
});

if (hasError) {
  process.exit(1);
} else {
  console.log('All agent manifests are valid!');
}
