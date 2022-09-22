Code to run the neopixel lights and the wifi AP for my hat.

```
█████   █████            █████         █████████                       █████                       ████ 
░███   ░░███            ░░███         ███░░░░░███                     ░░███                       ░░███ 
░███    ░███   ██████   ███████      ███     ░░░   ██████  ████████   ███████   ████████   ██████  ░███ 
░███████████  ░░░░░███ ░░░███░      ░███          ███░░███░░███░░███ ░░░███░   ░░███░░███ ███░░███ ░███ 
░███░░░░░███   ███████   ░███       ░███         ░███ ░███ ░███ ░███   ░███     ░███ ░░░ ░███ ░███ ░███ 
░███    ░███  ███░░███   ░███ ███   ░░███     ███░███ ░███ ░███ ░███   ░███ ███ ░███     ░███ ░███ ░███ 
█████   █████░░████████  ░░█████     ░░█████████ ░░██████  ████ █████  ░░█████  █████    ░░██████  █████
░░░░░   ░░░░░  ░░░░░░░░    ░░░░░       ░░░░░░░░░   ░░░░░░  ░░░░ ░░░░░    ░░░░░  ░░░░░      ░░░░░░  ░░░░░ 
                                                                                                        
Welcome to Hat Control. Come visit us in the Exploit Village.

Type   help   to see a list of commands.                                                                                             
    
> help
List of command:
color [color]   - sets color of lights. 
                    Choose from red, orange, yellow, green, blue, ...
method [method] - sets animation of lights.
                    Choosee from random, sparkle, wheel, pulse, ...
bright [level]  - sets brightness of lights.
                    Choose from low, medium, high
help            - shows this list

Console allows tab completion and listing choices with [command] <double tab>
> color 
red     orange      yellow      green       blue        purple      pink        white       rainbow     hot     cool        jet     bone
> color jet
set color to jet
> method 
random      sparkle     wheel       chase       pulse       wipe
> method random
set method to random
> bright 
low     medium      high
> bright low
set brightness to low
>
```