<div class="text-center">
    <h2 class="text-2xl font-bold text-gray-800">Chào mừng Thí sinh!</h2>
    <p class="mt-2 text-gray-600">Mã tài khoản: {{ $candidate->MaTK ?? 'N/A' }}</p>
    <p class="text-gray-600">Email: {{ $candidate->Email ?? 'N/A' }}</p>

    <div class="mt-8 space-y-4">
        <a href="{{ route('candidate.profile') }}"
           class="block w-full bg-blue-600 text-white py-3 px-6 rounded-lg hover:bg-blue-700 font-medium">
            Cập nhật hồ sơ
        </a>
        <a href="{{ route('candidate.apply') }}"
           class="block w-full bg-green-600 text-white py-3 px-6 rounded-lg hover:bg-green-700 font-medium">
            Nộp hồ sơ xét tuyển
        </a>
        <a href="{{ route('candidate.status') }}"
           class="block w-full bg-gray-600 text-white py-3 px-6 rounded-lg hover:bg-gray-700 font-medium">
            Theo dõi trạng thái
        </a>
    </div>
</div>
