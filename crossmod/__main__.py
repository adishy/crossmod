from crossmod.ml.subreddit_monitor import CrossmodSubredditMonitor
from crossmod.ml.classifiers import CrossmodClassifiers
from crossmod.crossmod_gunicorn import CrossmodGunicorn
from pyfiglet import Figlet
import click
import crossmod
from threading import Thread

def load_classifiers():
  crossmod.clf_ensemble = CrossmodClassifiers()

@click.command()
@click.argument('mode')
def main(mode):
  crossmod_ascii_banner = Figlet(font='graffiti')
  print(crossmod_ascii_banner.renderText('crossmod'))
  if mode == "api":
    print("API\n")
    options = {
      'preload_app': True,
      'workers': 3,
      'debug': True
    }
    thread = Thread(target= load_classifiers )
    thread.start()
    CrossmodGunicorn(crossmod.app, options).run()

  elif mode == "monitor":
    print("Monitor\n")
    subreddit_monitor = CrossmodSubredditMonitor()
    subreddit_monitor.monitor()

if __name__=="__main__":
  main()