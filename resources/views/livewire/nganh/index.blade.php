<div>
    <h2 class="text-2xl font-bold mb-6 text-gray-800">Danh sách Ngành</h2>
    <table class="w-full bg-white rounded-lg shadow overflow-hidden">
        <thead class="bg-green-900 text-white">
            <tr>
                <th class="px-6 py-3 text-left">Mã Ngành</th>
                <th class="px-6 py-3 text-left">Tên Ngành</th>
                <th class="px-6 py-3 text-left">Khoa</th>
            </tr>
        </thead>
        <tbody>
            @forelse ($nganhs as $nganh)
                <tr class="border-b hover:bg-gray-50">
                    <td class="px-6 py-3 font-medium">{{ $nganh['ma_nganh'] }}</td>
                    <td class="px-6 py-3">{{ $nganh['ten_nganh'] }}</td>
                    <td class="px-6 py-3">{{ $nganh['khoa']['ten_khoa'] ?? 'N/A' }}</td>
                </tr>
            @empty
                <tr>
                    <td colspan="3" class="px-6 py-4 text-center text-gray-500">Chưa có ngành nào.</td>
                </tr>
            @endforelse
        </tbody>
    </table>
</div>
