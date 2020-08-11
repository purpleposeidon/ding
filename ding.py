#!/usr/bin/python3

"""
This is a simple training counter program.

Depends on:
    mpv
    espeak


Suggested i3 configuration:

    bindsym $mod+Home               exec "ding   score++   "
    bindsym $mod+End                exec "ding   score--   "
    bindsym $mod+Shift+Home         exec "ding   score?    "
    bindsym $mod+Shift+End          exec "ding   reset     "
    bindsym $mod+Ctrl+Shift+Home    exec "ding   goal++    "
    bindsym $mod+Ctrl+Shift+End     exec "ding   goal--    "

"""

DEFAULT_GOAL = 6
RESET_TIME = 60 * 30 # half an hour

import sys, os, time

filename = os.path.expanduser("~/.cache/ding")

base = os.path.dirname(os.path.realpath(__file__))
os.chdir(base)



try: f = open(filename, 'r').read().strip()
except: f = ''

def say(a):
    print(a)
    os.system("echo %r | espeak -a 50 &" % a)

def play(a):
    # mplayer -volume 100 a
    cmd = "mpv ./%s.mp3 &" % a
    os.system(cmd)

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

def cmd(*variants):
    for a in variants:
        if a in sys.argv: return True

if cmd("reset", "0"):
    n = 0
    save()
    say("Reset")
elif cmd("score++", "+"):
    n += 1
    print("{} / {}".format(n, goal))
    if n >= goal:
        n = 0
        play("ding_win")
        n = 0
    else:
        play("ding_incr")
    save()
elif cmd("score--", "-"):
    n -= 1
    print("{} / {}".format(n, goal))
    if n < 0:
        n = 0
        play("ding_negative")
    else:
        play("ding_decr")
    save()
elif cmd("goal++", "goal--"):
    if cmd("goal++"):
        goal += 1
    else:
        goal -= 1
    if goal < 2:
        goal = 2
    save()
    say("goal is " + str(goal))
elif cmd("score?", "?"):
    say("score is " + str(n) + " out of " + str(goal))
else:
    print("See source for usage.")
