
screen getAPIKeyField:
    vbox:
        xalign 0.5
        yalign 0.5
        text "Submit your API Key (leave empty to cancel)":
            size 20
            xalign 0.5

        input default "":
            length 52
            value VariableInputValue("inputValue")
            xalign 0.5
            copypaste True

        textbutton "SUMBIT":
            action Jump("getAPIKey.check")
            keysym('K_RETURN', 'K_KP_ENTER')
            xalign 0.5

label getAPIKey:
    $ quick_menu = False
    $ inputValue = ""
    show screen getAPIKeyField
    $ ui.interact()

label .check:
    hide screen getAPIKeyField
    if not inputValue.strip() == "":
        $ persistent.apiKey = inputValue.strip()
    jump checkLogin
