<?php

return [
    'layouts' => [
        'title' => null,
    ],

    'assets' => [
        'is_livewire_loaded' => true,
    ],

    'back_button_deprecated' => env('LIVEWIRE_BACK_BUTTON_DEPRECATED', false),
    'temporary_file_upload' => env('LIVEWIRE_TEMPORARY_FILE_UPLOAD', true),
    'persist_navigation' => env('LIVEWIRE_PERSIST_NAVIGATION', true),
    'render_on_lazy_loaded' => true,
    'default_class_saving_path' => null,
    'manifest' => null,
];
