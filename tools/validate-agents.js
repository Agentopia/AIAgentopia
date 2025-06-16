// validate-agents.js
// Scans all agent.json files in agents/ and validates them against agent-manifest.schema.json
// Usage: node tools/validate-agents.js [path/to/specific/agent.json]
// If no path is provided, it scans all agent.json files in agents/.

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
const manifestSchema = schema; // Rename for clarity within function scopes

function validateSingleManifest(manifestPath) {
  // Validate a single agent.json file
  if (!fs.existsSync(manifestPath)) {
    console.error(`❌ Error: Manifest file not found at ${manifestPath}`);
    hasError = true;
    return;
  }
  const agentDir = path.dirname(manifestPath);


  try {
    const manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf-8'));
    const valid = validate(manifest); // 'validate' is the compiled schema validator from ajv
    if (!valid) {
      hasError = true;
      console.error(`❌ Schema validation failed for ${manifestPath}`);
      console.error('Validation errors:', JSON.stringify(validate.errors, null, 2));
    } else {
      console.log(`✅ Schema validation successful for ${manifestPath}.`);
      // Perform additional content sanity checks if schema is valid
      if (!manifest.name || manifest.name.trim() === "") {
        hasError = true;
        console.error(`❌ Content Error [${manifestPath}]: 'name' field should not be empty.`);
      }
      if (!manifest.long_description || manifest.long_description.trim().length < 50) {
        hasError = true;
        console.error(`❌ Content Error [${manifestPath}]: 'long_description' is too short (min 50 chars). Current: ${manifest.long_description?.trim().length || 0}`);
      }
      if (!manifest.docker_image_name || manifest.docker_image_name.trim() === "") {
        hasError = true;
        console.error(`❌ Content Error [${manifestPath}]: 'docker_image_name' should not be empty.`);
      }
      if (!manifest.docker_run_instructions || manifest.docker_run_instructions.trim().length < 100 || !manifest.docker_run_instructions.toLowerCase().includes('docker run')) {
        hasError = true;
        console.error(`❌ Content Error [${manifestPath}]: 'docker_run_instructions' seems too short or doesn't include 'docker run' (min 100 chars). Current: ${manifest.docker_run_instructions?.trim().length || 0}`);
      }

      if (manifest.llm_dependency) {
        const llm = manifest.llm_dependency;
        const keyProviders = ["openai", "anthropic", "google", "cohere", "huggingface_api"];
        if (keyProviders.includes(llm.type) && (!llm.apiKeyEnvVar || llm.apiKeyEnvVar.trim() === "")) {
          hasError = true;
          console.error(`❌ Content Error [${manifestPath}]: 'llm_dependency.apiKeyEnvVar' is required when llm_dependency.type is '${llm.type}'.`);
        }
        if (llm.type === "local_api" && (!llm.apiEndpointEnvVar || llm.apiEndpointEnvVar.trim() === "")) {
          hasError = true;
          console.error(`❌ Content Error [${manifestPath}]: 'llm_dependency.apiEndpointEnvVar' is required when llm_dependency.type is 'local_api'.`);
        }
      }

      const deploymentStatus = manifest.deployment_status || manifestSchema.properties.deployment_status.default;
      if (deploymentStatus === "review" || deploymentStatus === "production") {
        if (!manifest.privacy_considerations || manifest.privacy_considerations.trim().length < 30) {
          hasError = true;
          console.error(`❌ Content Error [${manifestPath}]: 'privacy_considerations' is required and should be substantial for agents in '${deploymentStatus}' status (min 30 chars). Current: ${manifest.privacy_considerations?.trim().length || 0}`);
        }
        if (!manifest.use_cases || manifest.use_cases.length === 0) {
            hasError = true;
            console.error(`❌ Content Error [${manifestPath}]: 'use_cases' should not be empty for agents in '${deploymentStatus}' status.`);
        }
      }
      // Add more checks here as needed

      if (!hasError) { // Only log individual success if no content errors were found for this file
        // This specific console.log might be too verbose if scanning many files and one has an error.
        // Consider moving the final success message outside the loop for batch processing.
      }
    }
  } catch (err) {
    if (err instanceof SyntaxError) {
      hasError = true;
      console.error(`❌ JSON parsing error in ${manifestPath}: ${err.message}`);
    } else {
      hasError = true;
      console.error(`❌ Unexpected error processing ${manifestPath}: ${err.message}`);
      console.error(err.stack || err);
    }
  }
}

// Main execution logic
const specificManifestPath = process.argv[2];

if (specificManifestPath) {
  const absolutePath = path.resolve(specificManifestPath);
  console.log(`Validating specific manifest: ${absolutePath}`);
  validateSingleManifest(absolutePath);
} else {
  console.log(`Scanning all agent manifests in ${agentsDir}...`);
  fs.readdirSync(agentsDir).forEach(agentFolder => {
  const agentPath = path.join(agentsDir, agentFolder);
  const agentFolderPath = path.join(agentsDir, agentFolder);
  if (fs.statSync(agentFolderPath).isDirectory()) {
    const manifestFilePath = path.join(agentFolderPath, 'agent.json');
    // Call validateSingleManifest for each found agent.json
    // The original validateAgentManifest took a directory; adapting to take a file path.
    validateSingleManifest(manifestFilePath);
  }
});
} // End of else block for scanning all agents

if (hasError) {
  process.exit(1);
} else {
  if (!hasError) console.log('✅ All scanned agent manifests are valid!');
}
