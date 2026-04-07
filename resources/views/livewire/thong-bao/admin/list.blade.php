<div>
    <h2 class="text-2xl font-bold mb-6 text-gray-800">Danh sách thông báo đã gửi</h2>
    <table class="w-full bg-white rounded-lg shadow overflow-hidden">
        <thead class="bg-blue-900 text-white">
            <tr>
                <th class="px-6 py-3 text-left">Mã TB</th>
                <th class="px-6 py-3 text-left">Nội dung</th>
                <th class="px-6 py-3 text-center">Ngày gửi</th>
                <th class="px-6 py-3 text-left">Người gửi</th>
            </tr>
        </thead>
        <tbody>
            @forelse ($thongBaos as $tb)
                <tr class="border-b hover:bg-gray-50">
                    <td class="px-6 py-3 font-medium">{{ $tb['ma_tb'] }}</td>
                    <td class="px-6 py-3">{{ $tb['noi_dung'] }}</td>
                    <td class="px-6 py-3 text-center">{{ $tb['ngay_gui'] }}</td>
                    <td class="px-6 py-3">{{ $tb['quan_tri']['ten_dn'] ?? 'N/A' }}</td>
                </tr>
            @empty
                <tr>
                    <td colspan="4" class="px-6 py-4 text-center text-gray-500">Chưa có thông báo nào.</td>
                </tr>
            @endforelse
        </tbody>
    </table>
</div>
