<div>
    <h2 class="text-2xl font-bold mb-6 text-gray-800">Hồ sơ Sinh viên</h2>
    @if ($student)
        <div class="bg-white p-6 rounded-lg shadow max-w-md">
            <div class="mb-4">
                <span class="text-gray-500">Mã SV:</span>
                <span class="ml-2 font-medium">{{ $student['ma_sv'] }}</span>
            </div>
            <div class="mb-4">
                <span class="text-gray-500">Họ tên:</span>
                <span class="ml-2 font-medium">{{ $student['ho_ten'] }}</span>
            </div>
            <div class="mb-4">
                <span class="text-gray-500">Email:</span>
                <span class="ml-2 font-medium">{{ $student['email'] }}</span>
            </div>
            <div class="mb-4">
                <span class="text-gray-500">Lớp:</span>
                <span class="ml-2 font-medium">{{ $student['lop']['ten_lop'] ?? 'Chưa xếp lớp' }}</span>
            </div>
        </div>
    @endif
</div>
