# ATO (自動列車運転装置) に関するソースコード群

駅での停車・発車を実現するために、列車の速度を指示する。

IEEE 1474 規格において定義されている CBTC は、自動列車管理装置、自動列車運転装置、自動列車防護装置(ATP 装置)より構成されている。

このコードは、自動列車運転装置の役割を担うことを目的としている。**※現時点では、control.py の `calc_speed()` 関数内で実装しています。のちのち独立したモジュールとして切り出すかもしれません**

## やること
- 停車駅の情報から、停止位置を取得する（←運転士がホーム脇に掲示されている停止位置目標を見ることに相当）
- ATPから許容速度を取得する（←運転士が信号機を見ることに相当）
- 許容速度の範囲内で、停止位置で止まるための速度を計算する（←運転士が駅でぴったり止まるように電車を操作することに相当）