<div>
    <h2 class="text-2xl font-bold mb-6 text-gray-800">Danh sách Lớp</h2>
    <table class="w-full bg-white rounded-lg shadow overflow-hidden">
        <thead class="bg-indigo-900 text-white">
            <tr>
                <th class="px-6 py-3 text-left">Mã Lớp</th>
                <th class="px-6 py-3 text-left">Tên Lớp</th>
                <th class="px-6 py-3 text-left">Ngành</th>
            </tr>
        </thead>
        <tbody>
            @forelse ($lops as $lop)
                <tr class="border-b hover:bg-gray-50">
                    <td class="px-6 py-3 font-medium">{{ $lop['ma_lop'] }}</td>
                    <td class="px-6 py-3">{{ $lop['ten_lop'] }}</td>
                    <td class="px-6 py-3">{{ $lop['nganh']['ten_nganh'] ?? 'N/A' }}</td>
                </tr>
            @empty
                <tr>
                    <td colspan="3" class="px-6 py-4 text-center text-gray-500">Chưa có lớp nào.</td>
                </tr>
            @endforelse
        </tbody>
    </table>
</div>
