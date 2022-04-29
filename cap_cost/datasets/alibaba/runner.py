"""
Script to be able to debug the crawler
https://stackoverflow.com/questions/49201915/debugging-scrapy-project-in-visual-studio-code

"""
if __name__ == '__main__':

    import os
    from scrapy.cmdline import execute

    os.chdir(os.path.dirname(os.path.realpath(__file__)))

    try:
        execute(
            [
                'scrapy',
                'crawl',
                'alibaba_crawler',
            ]
        )
    except SystemExit:
        pass
