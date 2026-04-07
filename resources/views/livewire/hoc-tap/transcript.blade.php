<div>
    <h2 class="text-2xl font-bold mb-6 text-gray-800">Bảng điểm & GPA</h2>

    <div class="bg-white p-4 rounded-lg shadow mb-6">
        <span class="text-gray-600">GPA hiện tại:</span>
        <span class="ml-2 text-2xl font-bold text-blue-600">{{ number_format($gpa, 2) }}</span>
        <span class="text-gray-500 text-sm">/ 4.00</span>
    </div>

    <table class="w-full bg-white rounded-lg shadow overflow-hidden">
        <thead class="bg-blue-900 text-white">
            <tr>
                <th class="px-6 py-3 text-left">Mã môn</th>
                <th class="px-6 py-3 text-left">Tên môn học</th>
                <th class="px-6 py-3 text-center">Số tín chỉ</th>
                <th class="px-6 py-3 text-center">Điểm</th>
            </tr>
        </thead>
        <tbody>
            @forelse ($transcript as $item)
                <tr class="border-b">
                    <td class="px-6 py-3">{{ $item['ma_mh'] }}</td>
                    <td class="px-6 py-3">{{ $item['mon_hoc']['ten_mh'] ?? 'N/A' }}</td>
                    <td class="px-6 py-3 text-center">{{ $item['mon_hoc']['so_tin_chi'] ?? 0 }}</td>
                    <td class="px-6 py-3 text-center font-bold">{{ number_format($item['diem'], 2) }}</td>
                </tr>
            @empty
                <tr>
                    <td colspan="4" class="px-6 py-4 text-center text-gray-500">Chưa có điểm.</td>
                </tr>
            @endforelse
        </tbody>
    </table>
</div>
