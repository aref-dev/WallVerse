from setuptools import setup, find_packages

setup(
    name='wallverse',
    version='0.1.0',
    url='https://github.com/aref-dev/WallVerse',
    license='MIT',
    author='Aref Nasrollah Zadeh',
    author_email='aref.anz@outlook.com',
    description='Random Topic Based Quotations as Your Wallpaper',
    long_description=''.join(open('README.md', encoding='utf-8').readlines()),
    long_description_content_type='text/markdown',
    keywords=['wallpaper', 'quotes', 'multiplatform', 'desktop customization', 'motivational', 'wisdom', 'funny'],
    packages=["wallverse"],
    package_data={
        'wallverse': [
            '*',
            'ui_resources/*',
            'ui_resources/background_images/*',
            'ui_resources/fonts/*'
        ]
    },
    include_package_data=True,
    install_requires=[
        'arabic-reshaper==3.0.0',
        'cowsay==6.1',
        'CTkColorPicker==0.8.0',
        'customtkinter==5.2.1',
        'darkdetect==0.8.0',
        'packaging==23.2',
        'Pillow==10.1.0',
        'pystray==0.19.5',
        'python-bidi==0.4.2',
        'screeninfo==0.8.1',
        'pypiwin32 == 223',
        'winshell == 0.6',
        'fonttools==4.45.1'
    ],
    python_requires='>=3.10',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: MacOS X',
        'Environment :: Win32 (MS Windows)',
        'Environment :: X11 Applications',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.10',
        'Topic :: Desktop Environment',
        'Topic :: Utilities',
    ],
    entry_points={
        'console_scripts': [
            'wallverse=wallverse.main:run',
        ],
    }
)
