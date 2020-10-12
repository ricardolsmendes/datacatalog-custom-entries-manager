import setuptools

setuptools.setup(
    name='datacatalog-custom-entries-manager',
    version='0.1.0',
    url='https://github.com/ricardolsmendes/datacatalog-custom-entries-manager',
    author='Ricardo Mendes',
    author_email='ricardolsmendes@gmail.com',
    license='MIT',
    description='A package to manage Google Cloud Data Catalog custom entries',
    platforms='Posix; MacOS X; Windows',
    packages=setuptools.find_packages(where='./src'),
    package_dir={'': 'src'},
    entry_points={
        'console_scripts': [
            'datacatalog-custom-entries = datacatalog_custom_entries_manager:main',
        ],
    },
    include_package_data=True,
    install_requires=(
        'google-datacatalog-connectors-commons',
        'pandas',
    ),
    setup_requires=('pytest-runner', ),
    tests_require=('pytest-cov', ),
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
