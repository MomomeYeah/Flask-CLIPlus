_cli_plus()
{
    local words cur opts
    COMPREPLY=()

    # all tokens we've entered so far
    words="${COMP_WORDS[@]}"
    # the last token we entered
    cur="${COMP_WORDS[COMP_CWORD]}"

    #echo "cword is ${COMP_CWORD}"
    #echo "asda: ${words} - ${cur}"

    # the list of autocomplete suggestions we generate
    opts=$(python /vagrant/project/cli_plus.py ${words})

    #echo "opts is ${opts}"

    COMPREPLY=( $(compgen -W "${opts}" -- ${cur}) )
    return 0
}

complete -F _cli_plus ./autocomplete.py
