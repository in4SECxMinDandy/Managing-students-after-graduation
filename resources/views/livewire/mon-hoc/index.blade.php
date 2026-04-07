<div>
    <h2 class="text-2xl font-bold mb-6 text-gray-800">Danh sách Môn học</h2>
    <table class="w-full bg-white rounded-lg shadow overflow-hidden">
        <thead class="bg-orange-900 text-white">
            <tr>
                <th class="px-6 py-3 text-left">Mã Môn</th>
                <th class="px-6 py-3 text-left">Tên Môn học</th>
                <th class="px-6 py-3 text-center">Số tín chỉ</th>
            </tr>
        </thead>
        <tbody>
            @forelse ($monHocs as $mh)
                <tr class="border-b hover:bg-gray-50">
                    <td class="px-6 py-3 font-medium">{{ $mh['ma_mh'] }}</td>
                    <td class="px-6 py-3">{{ $mh['ten_mh'] }}</td>
                    <td class="px-6 py-3 text-center">{{ $mh['so_tin_chi'] }}</td>
                </tr>
            @empty
                <tr>
                    <td colspan="3" class="px-6 py-4 text-center text-gray-500">Chưa có môn học nào.</td>
                </tr>
            @endforelse
        </tbody>
    </table>
</div>
