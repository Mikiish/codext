### Toolset to format embedded $LaTeX$ from pasting ChatGPT mess...
Sometimes ChatGPT escape all special character because it doesn't understand that the LaTeX compiler fails because of unicode chars. Here is how you can easily clean up. We remove all escapes from litterals `\_`, `\[`, and `\$` then we fix unicodes errors by hands or with agents workflow. Usually doing it by hands is faster and safer...

- Install dependencies with `./latex_deps.sh`
- Copy the message from the copy button right down the message in the ChatGPT web-app (DeepSearch UI).
- Paste it in a new `raw.md` file.
- Execute the `fix_latex_escapes.js`. (just run `node fix_latex_escapes.js`)
- Execute the command down below. It will bugs out for every problematic unicode characters.
- Fix theim all one by one or send agents, at your own risks, kek...
- Repeat the pandoc command until it works xD.

```bash
pandoc raw_fixed.md -s -o synthese.pdf --pdf-engine=pdflatex -V geometry:margin=1in
```