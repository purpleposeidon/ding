#!/usr/bin/python3

"""
This is a simple training counter program.


i3 config:

    bindsym $mod+Shift+Home exec "ding ="
    bindsym $mod+Home exec "ding +"
    bindsym $mod+End exec "ding -"
    bindsym $mod+Shift+End exec "ding 0"

"""

DEFAULT_GOAL = 6
RESET_TIME = 60 * 30 # half an hour

import sys, os, time

filename = os.path.expanduser("~/.cache/ding")


try: f = open(filename, 'r').read().strip()
except: f = ''

def say(a):
    os.system("echo %r | espeak -a 50 &" % a)
    raise SystemExit

def play(a):
    # mplayer -volume 100 a
    cmd = "mpv ~/Development/ding/%s.mp3 &" % a
    os.system(cmd)
    print(cmd)

def save():
    open(filename, 'w').write("{n} {goal} {last}\n".format(**globals()))

now = int(time.time())

try: n, goal, last = map(int, f.split())
except:
    n, goal, last = (0, DEFAULT_GOAL, now)
    save()
    say("reset. file missing.")

if last + RESET_TIME < now:
    save()
    say("starting over, score too old")

if '0' in sys.argv:
    n = 0
    save()
    say("Reset")
elif '+' in sys.argv:
    n += 1
    print("{} / {}".format(n, goal))
    if n >= goal:
        n = 0
        play("ding_win")
        n = 0
    else:
        play("ding_incr")
    save()
elif '-' in sys.argv:
    n -= 1
    print("{} / {}".format(n, goal))
    if n < 0:
        n = 0
        play("ding_negative")
    else:
        play("ding_decr")
    save()
else:
    say("score is " + str(n) + " out of " + str(goal))

