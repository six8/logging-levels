from distutils.core import setup

def main():
    setup(
        name = 'logging_levels',
        packages=['logging_levels'],
        package_dir = {'logging_levels':'logging_levels'},
        version = open('VERSION.txt').read().strip(),
        author='Mike Thornton',
        author_email='six8@devdetails.com',
        url='https://github.com/six8/logging-levels',
        download_url='https://github.com/six8/logging-levels',
        keywords=['logging'],
        license='MIT',
        description="Add convenient logging levels for when DEBUG just isn't enough.",
        classifiers = [
            "Programming Language :: Python",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python :: 2.6",
            "Programming Language :: Python :: 2.7",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.2",
            "Programming Language :: Python :: 3.3",          
            "Topic :: Software Development :: Libraries :: Python Modules",
        ],
        long_description=open('README.rst').read(),
    )

if __name__ == '__main__':
    main()