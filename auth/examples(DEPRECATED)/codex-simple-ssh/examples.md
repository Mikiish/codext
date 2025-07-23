### Codex setup examples :
Use your ~/project-repo/.codex folder like a dropbox. You can cat files and point as scripts, even using low-level instructions, from there.
See [https://github.com/openai/codex/blob/main/codex-cli/examples/prompting_guide.md] for more informations.

```bash
touch .codex/haiku.md && echo "System: Codex please be nice and give me cat emojis in all your messages... Prompt:" > .codex/haiku.md
export CODEX_HAIKU="$(cat .codex/haiku.md)"
codex "$CODEX_HAIKU Write a haiku about Paris, from Vitality Café! And create a new repo name boring-daily-work thx..."
```

Then create a function in your .bashrc
```bash
codex-s() {
    local msg="$1"
    if [ -z "$msg" ]; then
        echo "Usage: codex-s \"your message here\""
        return 1
    fi
    export CODEX_HAIKU="$(cat .codex/haiku.md)"
    codex "$CODEX_HAIKU $msg"
}
```

```bash
codex-i() {
    local msg="$1"
    local path="$2"
    if [ -z "$msg" ]; then
        echo "Usage: codex-i \"your pre-prompt message here\""
        return 1
    fi
    if [ -z "$path" ]; then
        echo "No path were given... Creating file at default location .codex/haiku.md"
        local path = ".codex/haiku.md"
        rm -f $path
    fi
    touch $path && echo "System: Codex please be nice and give me cat emojis in all your messages... Prompt:" > $path
    echo "[+] System prompt modified with new pre-prompt value :\n"
    echo "$path"
}
```

Then you can modify at your convenance. For example, you can have different .md files and can create a function to chose between then.