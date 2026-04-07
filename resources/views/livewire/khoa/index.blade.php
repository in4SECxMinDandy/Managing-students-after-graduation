<div>
    <h2 class="text-2xl font-bold mb-6 text-gray-800">Danh sách Khoa</h2>

    @if (session('success'))
        <div class="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded mb-4">
            {{ session('success') }}
        </div>
    @endif

    <a href="{{ route('admin.khoa.create') }}"
       class="inline-block mb-4 bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 font-medium">
        + Thêm Khoa mới
    </a>

    <table class="w-full bg-white rounded-lg shadow overflow-hidden">
        <thead class="bg-blue-900 text-white">
            <tr>
                <th class="px-6 py-3 text-left">Mã Khoa</th>
                <th class="px-6 py-3 text-left">Tên Khoa</th>
                <th class="px-6 py-3 text-center">Số ngành</th>
                <th class="px-6 py-3 text-center">Thao tác</th>
            </tr>
        </thead>
        <tbody>
            @forelse ($khoas as $khoa)
                <tr class="border-b hover:bg-gray-50">
                    <td class="px-6 py-3 font-medium">{{ $khoa['ma_khoa'] }}</td>
                    <td class="px-6 py-3">{{ $khoa['ten_khoa'] }}</td>
                    <td class="px-6 py-3 text-center">{{ count($khoa['nganhs'] ?? []) }}</td>
                    <td class="px-6 py-3 text-center space-x-2">
                        <a href="{{ route('admin.khoa.edit', $khoa['ma_khoa']) }}"
                           class="text-blue-600 hover:underline">Sửa</a>
                        <button wire:click="deleteKhoa('{{ $khoa['ma_khoa'] }}')"
                            onclick="return confirm('Bạn có chắc muốn xóa?')"
                            class="text-red-600 hover:underline">Xóa</button>
                    </td>
                </tr>
            @empty
                <tr>
                    <td colspan="4" class="px-6 py-4 text-center text-gray-500">Chưa có khoa nào.</td>
                </tr>
            @endforelse
        </tbody>
    </table>
</div>
