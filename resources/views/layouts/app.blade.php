<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="csrf-token" content="{{ csrf_token() }}">
    <title>@yield('title', 'QLSVSDH')</title>
    @livewireStyles
    @vite(['resources/css/app.css', 'resources/js/app.js'])
</head>
<body class="bg-gray-100 font-sans antialiased">
    @auth('admin')
        @include('layouts._admin_navbar')
    @endauth

    <main class="min-h-screen">
        @yield('content')
        @isset($slot)
            {{ $slot }}
        @endisset
    </main>

    @livewireScripts
</body>
</html>
