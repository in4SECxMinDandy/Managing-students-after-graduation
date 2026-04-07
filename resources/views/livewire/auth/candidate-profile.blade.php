<div class="max-w-lg mx-auto p-6">
    <h2 class="text-2xl font-bold text-gray-800 mb-4">Hồ sơ thí sinh</h2>

    @if ($hso)
        <dl class="space-y-2 text-gray-700">
            <dt class="font-medium">Họ tên</dt>
            <dd>{{ $hso->HoTen }}</dd>
            <dt class="font-medium">CCCD</dt>
            <dd>{{ $hso->CCCD }}</dd>
            <dt class="font-medium">SĐT</dt>
            <dd>{{ $hso->SDT }}</dd>
        </dl>
    @else
        <p class="text-gray-600">Chưa có hồ sơ. Vui lòng hoàn tất đăng ký hoặc liên hệ quản trị.</p>
    @endif

    <a href="{{ route('candidate.dashboard') }}" class="mt-6 inline-block text-blue-600 hover:underline">← Về trang chủ thí sinh</a>
</div>
