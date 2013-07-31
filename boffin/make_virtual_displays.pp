package { ['xvfb',
                        'x11-xkb-utils',
                        'xfonts-100dpi',
                        'xfonts-75dpi',
                        'xfonts-scalable',
                        'xfonts-cyrillic',
                        'xserver-xorg-core']:
             ensure  => latest,
}
exec {'Create new virtual desktop1':
                         require  => [ Package['xvfb'],
                                      Package['x11-xkb-utils'],
                                      Package['xfonts-100dpi'],
                                      Package['xfonts-75dpi'],
                                      Package['xfonts-scalable'],
                                      Package['xfonts-cyrillic'],
                                      Package['xserver-xorg-core'] ],
                         command  => 'Xvfb -fp /usr/share/fonts/X11/misc/ :20
                          -screen 0 1024x768x16 2>&1; echo "ok"',
                         user     => 'root',
                         provider => shell,
                         path     => '/usr/bin',
}
exec {'Create new virtual desktop2':
                         require  => [ Package['xvfb'],
                                      Package['x11-xkb-utils'],
                                      Package['xfonts-100dpi'],
                                      Package['xfonts-75dpi'],
                                      Package['xfonts-scalable'],
                                      Package['xfonts-cyrillic'],
                                      Package['xserver-xorg-core'] ],
                         command  => 'Xvfb -fp /usr/share/fonts/X11/misc/ :21
                          -screen 1 1024x768x16 2>&1; echo "ok"',
                         user     => 'root',
                         provider => shell,
                         path     => '/usr/bin',
}
exec {'Create new virtual desktop3':
                         require  => [ Package['xvfb'],
                                      Package['x11-xkb-utils'],
                                      Package['xfonts-100dpi'],
                                      Package['xfonts-75dpi'],
                                      Package['xfonts-scalable'],
                                      Package['xfonts-cyrillic'],
                                      Package['xserver-xorg-core'] ],
                         command  => 'Xvfb -fp /usr/share/fonts/X11/misc/ :22
                          -screen 2 1024x768x16 2>&1; echo "ok"',
                         user     => 'root',
                         provider => shell,
                         path     => '/usr/bin',
}
