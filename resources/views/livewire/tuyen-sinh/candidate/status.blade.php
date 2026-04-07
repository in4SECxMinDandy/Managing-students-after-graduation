<div>
    <h2 class="text-2xl font-bold mb-6 text-gray-800">Theo dõi trạng thái xét tuyển</h2>
    <table class="w-full bg-white rounded-lg shadow overflow-hidden">
        <thead class="bg-purple-900 text-white">
            <tr>
                <th class="px-6 py-3 text-left">Ngành</th>
                <th class="px-6 py-3 text-left">Phương thức</th>
                <th class="px-6 py-3 text-center">Điểm</th>
                <th class="px-6 py-3 text-center">Trạng thái</th>
            </tr>
        </thead>
        <tbody>
            @forelse ($applications as $app)
                <tr class="border-b">
                    <td class="px-6 py-3">{{ $app['nghanh']['ten_nganh'] ?? 'N/A' }}</td>
                    <td class="px-6 py-3">{{ $app['phuong_thuc'] }}</td>
                    <td class="px-6 py-3 text-center">{{ $app['diem'] }}</td>
                    <td class="px-6 py-3 text-center">
                        @if ($app['trang_thai'] === 'Đậu')
                            <span class="bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm">Đậu</span>
                        @elseif ($app['trang_thai'] === 'Rớt')
                            <span class="bg-red-100 text-red-800 px-3 py-1 rounded-full text-sm">Rớt</span>
                        @else
                            <span class="bg-yellow-100 text-yellow-800 px-3 py-1 rounded-full text-sm">Chờ duyệt</span>
                        @endif
                    </td>
                </tr>
            @empty
                <tr>
                    <td colspan="4" class="px-6 py-4 text-center text-gray-500">Chưa có hồ sơ nào.</td>
                </tr>
            @endforelse
        </tbody>
    </table>
</div>
