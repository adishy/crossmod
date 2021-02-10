from crossmod.ml.subreddit_monitor import CrossmodSubredditMonitor
from crossmod.ml.classifiers import CrossmodClassifiers
from crossmod.crossmod_gunicorn import CrossmodGunicorn
from pyfiglet import Figlet
import os
import sys
import click
import crossmod
from threading import Thread

def load_classifiers():
  crossmod.clf_ensemble = CrossmodClassifiers()
  sys.stdout.flush()
  sys.stderr.flush()

#@click.command()
#@click.argument('mode')
def main():
  crossmod_ascii_banner = Figlet(font='graffiti')
  print(crossmod_ascii_banner.renderText('crossmod'))
  #if mode == "api":
  print("API\n")
  port = 8000
  if os.environ.get("PORT"):
    port = os.environ["PORT"]
  options = \
  {
    'bind': f'127.0.0.1:{port}',
    'preload_app': True,
    'workers': 3,
    'debug': True
  }
  thread = Thread(target= load_classifiers )
  thread.start()
  CrossmodGunicorn(crossmod.app, options).run()

  #elif mode == "monitor":
    #print("Monitor\n")
    #subreddit_monitor = CrossmodSubredditMonitor()
    #subreddit_monitor.monitor()

if __name__=="__main__":
  main()