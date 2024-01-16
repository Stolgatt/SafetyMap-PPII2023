import cProfile
from app import app

if __name__ == "__main__":
    profiler = cProfile.Profile()
    profiler.enable()
    app.run()
    profiler.disable()
    profiler.dump_stats("flask_startup_profile.pstat")
