const vscode = require('vscode');
const { exec } = require('child_process');
const path = require('path');

function activate(context) {
  // Register the 'cpuasm.runAssembly' command
  let disposable = vscode.commands.registerCommand('cpuasm.runAssembly', function () {
    const editor = vscode.window.activeTextEditor;

    if (editor) {
      // Get the file name without extension (this should remove any extension)
      const fileName = path.basename(editor.document.uri.fsPath, path.extname(editor.document.uri.fsPath));

      // Set the directory path where the .cpuasm files are located
      const directory = 'C:\\Users\\Alex\\Downloads\\Code\\Python\\CPUAssembly\\Programs';
      
      // Construct the full path to the .cpuasm file
      const filePath = path.join(directory, `${fileName}`);

      // Construct the command
      const command = `cpuassemble ${filePath}`;

      // Execute the command
      exec(command, (error, stdout, stderr) => {
        if (error) {
          vscode.window.showErrorMessage(`Error: ${error.message}`);
          return;
        }
        if (stderr) {
          vscode.window.showErrorMessage(`stderr: ${stderr}`);
          return;
        }
        vscode.window.showInformationMessage(`Output: ${stdout}`);
      });
    }
  });

  // Push the disposable command to context subscriptions
  context.subscriptions.push(disposable);
}

function deactivate() {}

module.exports = {
  activate,
  deactivate
};
