import setuptools

setuptools.setup(
    name='datacatalog-custom-types-manager',
    version='0.0.1',
    url='https://github.com/ricardolsmendes/datacatalog-custom-types-manager',
    author='Ricardo Mendes',
    author_email='ricardolsmendes@gmail.com',
    license='MIT',
    description='A package to manage Google Cloud Data Catalog custom types',
    platforms='Posix; MacOS X; Windows',
    packages=setuptools.find_packages(where='./src'),
    package_dir={'': 'src'},
    entry_points={
        'console_scripts': [
            'datacatalog-custom-types = datacatalog_custom_types_manager:main',
        ],
    },
    include_package_data=True,
    install_requires=(
        'google-cloud-datacatalog',
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
