_cli_plus()
{
    local words cur opts
    COMPREPLY=()

    # all tokens we've entered so far
    words="${COMP_WORDS[@]}"
    # the last token we entered
    cur="${COMP_WORDS[COMP_CWORD]}"

    # call cli_plus.py with the list of words entered so far as our tokens.
    # `opts` will contain the list of autocomplete suggestions we generate
    opts=$(python /vagrant/cli_plus/cli_plus.py ${words})

    COMPREPLY=( $(compgen -W "${opts}" -- ${cur}) )
    return 0
}

# use the _cli_plus function above to provide bash autocompletion
# for the program `./sample.py`
complete -F _cli_plus ./sample.py
