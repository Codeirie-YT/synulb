const vscode = require("vscode");

function activate(context) {
    let run = vscode.commands.registerCommand("synulb.run", () => {
        const file = vscode.window.activeTextEditor.document.fileName;

        const terminal = vscode.window.createTerminal("Synulb");
        terminal.show();

        terminal.sendText(`synulb "${file}"`);
    });

    context.subscriptions.push(run);
}

function deactivate() {}

module.exports = {
    activate,
    deactivate
}