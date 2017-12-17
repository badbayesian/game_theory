from setuptools import setup


def main():
    setup(name='game_theory',
          version='0.1',
          description='Simple Game Theory simulation',
          url='https://github.com/badbayesian/game_theory',
          author='Daniel Silva-Inclan',
          author_email='badbayesian@gmail.com',
          license='MIT',
          packages=['game_theory'],
          zip_safe=False)


if __name__ == "__main__":
    main()
