<div>
    <h2 class="text-2xl font-bold mb-6 text-gray-800">Duyệt hồ sơ xét tuyển</h2>

    @if (session('success'))
        <div class="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded mb-4">
            {{ session('success') }}
        </div>
    @endif

    <table class="w-full bg-white rounded-lg shadow overflow-hidden">
        <thead class="bg-purple-900 text-white">
            <tr>
                <th class="px-6 py-3 text-left">Họ tên</th>
                <th class="px-6 py-3 text-left">Ngành</th>
                <th class="px-6 py-3 text-left">Phương thức</th>
                <th class="px-6 py-3 text-center">Điểm</th>
                <th class="px-6 py-3 text-center">Thao tác</th>
            </tr>
        </thead>
        <tbody>
            @forelse ($pendingApplications as $app)
                <tr class="border-b hover:bg-gray-50">
                    <td class="px-6 py-3 font-medium">{{ $app['hso_xet_tuyen']['ho_ten'] ?? 'N/A' }}</td>
                    <td class="px-6 py-3">{{ $app['nghanh']['ten_nganh'] ?? 'N/A' }}</td>
                    <td class="px-6 py-3">{{ $app['phuong_thuc'] }}</td>
                    <td class="px-6 py-3 text-center font-bold">{{ $app['diem'] }}</td>
                    <td class="px-6 py-3 text-center space-x-2">
                        <button wire:click="approve('{{ $app['ma_ptxt'] }}')"
                            class="bg-green-600 text-white px-3 py-1 rounded hover:bg-green-700 text-sm">
                            Duyệt
                        </button>
                        <button wire:click="reject('{{ $app['ma_ptxt'] }}')"
                            class="bg-red-600 text-white px-3 py-1 rounded hover:bg-red-700 text-sm">
                            Từ chối
                        </button>
                    </td>
                </tr>
            @empty
                <tr>
                    <td colspan="5" class="px-6 py-4 text-center text-gray-500">Không có hồ sơ chờ duyệt.</td>
                </tr>
            @endforelse
        </tbody>
    </table>
</div>
