<?php

return [
    'defaults' => [
        'guard' => 'web',
        'passwords' => 'users',
    ],

    'guards' => [
        'web' => [
            'driver' => 'session',
            'provider' => 'users',
        ],
        'candidate' => [
            'driver' => 'session',
            'provider' => 'candidates',
        ],
        'student' => [
            'driver' => 'session',
            'provider' => 'students',
        ],
        'admin' => [
            'driver' => 'session',
            'provider' => 'admins',
        ],
    ],

    'providers' => [
        'users' => [
            'driver' => 'eloquent',
            'model' => App\Models\User::class,
        ],
        'candidates' => [
            'driver' => 'eloquent',
            'model' => App\Modules\TuyenSinh\Models\TKXetTuyen::class,
        ],
        'students' => [
            'driver' => 'eloquent',
            'model' => App\Modules\SinhVien\Models\SinhVien::class,
        ],
        'admins' => [
            'driver' => 'eloquent',
            'model' => App\Modules\QuanTri\Models\QuanTri::class,
        ],
    ],

    'passwords' => [
        'users' => [
            'provider' => 'users',
            'table' => 'password_reset_tokens',
            'expire' => 60,
            'throttle' => 60,
        ],
    ],

    'password_timeout' => 10800,
];
