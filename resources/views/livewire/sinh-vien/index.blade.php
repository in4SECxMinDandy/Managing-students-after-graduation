<div>
    <h2 class="text-2xl font-bold mb-6 text-gray-800">Danh sách Sinh viên</h2>
    <table class="w-full bg-white rounded-lg shadow overflow-hidden">
        <thead class="bg-teal-900 text-white">
            <tr>
                <th class="px-6 py-3 text-left">Mã SV</th>
                <th class="px-6 py-3 text-left">Họ tên</th>
                <th class="px-6 py-3 text-left">Email</th>
                <th class="px-6 py-3 text-left">Lớp</th>
            </tr>
        </thead>
        <tbody>
            @forelse ($sinhViens as $sv)
                <tr class="border-b hover:bg-gray-50">
                    <td class="px-6 py-3 font-medium">{{ $sv['ma_sv'] }}</td>
                    <td class="px-6 py-3">{{ $sv['ho_ten'] }}</td>
                    <td class="px-6 py-3">{{ $sv['email'] }}</td>
                    <td class="px-6 py-3">{{ $sv['lop']['ten_lop'] ?? 'Chưa xếp lớp' }}</td>
                </tr>
            @empty
                <tr>
                    <td colspan="4" class="px-6 py-4 text-center text-gray-500">Chưa có sinh viên nào.</td>
                </tr>
            @endforelse
        </tbody>
    </table>
</div>
