import click
from crossmod.ml.subreddit_monitor import CrossmodSubredditMonitor
from crossmod.ml.classifiers import CrossmodClassifiers

@click.command()
@click.argument('mode')
def main(mode):
  if mode == "api":
    #crossmod.clf_ensemble = CrossmodClassifiers()
    print("API")

  elif mode == "monitor":
    print("Monitor")
    #subreddit_monitor = CrossmodSubredditMonitor()
    #subreddit_monitor.monitor()

if __name__ == "__main__":
  main()

