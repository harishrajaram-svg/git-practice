async function main() {
  const chunks = [];
  for await (const chunk of process.stdin) {
    chunks.push(chunk);
  }
  const toolArgs = JSON.parse(Buffer.concat(chunks).toString());

  // readPath is the path to the file that Claude is trying to read
  const readPath =
    toolArgs.tool_input?.file_path || toolArgs.tool_input?.path || "";

  // Block reading .env files
  const normalized = readPath.replace(/\\/g, "/");
  const filename = normalized.split("/").pop();

  if (filename === ".env" || filename.startsWith(".env.")) {
    console.error("Blocked: reading .env files is not allowed.");
    process.exit(2);
  }
}

main();
