import { spawn } from "node:child_process";

export interface ProcessResult {
  command: string;
  args: string[];
  exitCode: number | null;
  stdout: string;
  stderr: string;
}

export async function runProcess(
  command: string,
  args: string[],
  options: { cwd: string; timeoutMs?: number },
): Promise<ProcessResult> {
  return await new Promise((resolve) => {
    let settled = false;
    const child = spawn(command, args, {
      cwd: options.cwd,
      shell: false,
      windowsHide: true,
    });
    const timer = options.timeoutMs
      ? setTimeout(() => {
          if (settled) return;
          settled = true;
          child.kill();
          resolve({
            command,
            args,
            exitCode: -2,
            stdout,
            stderr: `Timed out after ${options.timeoutMs}ms`,
          });
        }, options.timeoutMs)
      : undefined;

    let stdout = "";
    let stderr = "";

    child.stdout.setEncoding("utf8");
    child.stderr.setEncoding("utf8");
    child.stdout.on("data", (chunk) => {
      stdout += chunk;
    });
    child.stderr.on("data", (chunk) => {
      stderr += chunk;
    });
    child.on("error", (error) => {
      if (settled) return;
      settled = true;
      if (timer) clearTimeout(timer);
      resolve({
        command,
        args,
        exitCode: -1,
        stdout,
        stderr: stderr + error.message,
      });
    });
    child.on("close", (exitCode) => {
      if (settled) return;
      settled = true;
      if (timer) clearTimeout(timer);
      resolve({ command, args, exitCode, stdout, stderr });
    });
  });
}

export async function runPython(
  args: string[],
  options: { cwd: string; timeoutMs?: number },
): Promise<ProcessResult> {
  const candidates =
    process.platform === "win32"
      ? [
          { command: "py", args: ["-3", ...args] },
          { command: "python", args },
          { command: "python3", args },
        ]
      : [
          { command: "python3", args },
          { command: "python", args },
        ];

  let lastResult: ProcessResult | undefined;
  for (const candidate of candidates) {
    const result = await runProcess(candidate.command, candidate.args, options);
    if (result.exitCode !== -1) return result;
    lastResult = result;
  }

  return (
    lastResult ?? {
      command: "python",
      args,
      exitCode: -1,
      stdout: "",
      stderr: "Python executable was not found.",
    }
  );
}
