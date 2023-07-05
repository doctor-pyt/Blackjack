import random

RANK, SUIT = 0, 1

# 勝敗判定　判定結果と計算後の持ちチップを返す
def win_lose(dealer_hand, player_hand, bet, player_money):
    player_point = get_point(player_hand)
    dealer_point = get_point(dealer_hand)
    if player_point <= 21:
        if (player_point > dealer_point) or (dealer_point > 21):
            if player_point == 21:
                return ("<<プレイヤーの勝ち>>", player_money + int(bet * 2.5))
            else:
                return ("<<プレイヤーの勝ち>>", player_money + int(bet * 2))
        elif player_point == dealer_point:
            return ("<<プッシュ>>", player_money + int(bet))
        else:
            return ("<<プレイヤーの負け>>", player_money)
    else:
        return ("<<プレイヤーの負け>>", player_money)


# プレイヤーの操作
def player_op(deck, player_hand, op):
    doubled, ending = False, False
    if op == "1":
        print("[ プレイヤー:スタンド ]")
        doubled, ending = False, True
    elif op == "2":
        print("[ プレイヤー:ヒット ]")
        player_hand.append(deck.pop())
        print_player_hand(player_hand)
        doubled, ending = False, False
    elif op == "3":
        if len(player_hand) == 2:  # 手札は2枚か
            print("[ プレイヤー:ダブル ]")
            player_hand.append(deck.pop())
            print_player_hand(player_hand)
            doubled, ending = True, True
        else:
            print("ダブルはできません")

    if get_point(player_hand) > 21:  # バスト判定
        print("[ プレイヤーはバストした ]")
        # break
        ending = True
    elif get_point(player_hand) == 21:
        print("ブラックジャックです")
        ending = True
    return doubled, ending


# ディーラーの操作
def dealer_op(deck, player_hand, dealer_hand):
    while get_point(player_hand) <= 21:
        if get_point(dealer_hand) >= 17:
            print("[ ディーラー:スタンド ]")
            break
        else:
            print("[ ディーラー:ヒット ]")
            dealer_hand.append(deck.pop())
        print_dealer_hand(dealer_hand, False)


# 手札のポイント計算
def get_point(hand):
    result = 0
    ace_flag = False
    for card in hand:
        if card[RANK] == 1:  # カードがAか？
            ace_flag = True
        if card[RANK] > 10:
            num = 10
        else:
            num = card[RANK]
        result += num
    if ace_flag and result <= 11:  # Aを含み11以下か？
        result += 10  # Aを11と考え+10
    return result


# プレイヤーの手札を表示
def print_player_hand(player_hand):
    print("プレイヤー (", get_point(player_hand), "):")
    for card in player_hand:
        print("[", card[SUIT], card[RANK], "]")
    print()


# ディーラーの手札を表示
def print_dealer_hand(dealer_hand, uncovered):
    if uncovered:
        print("ディーラー (", get_point(dealer_hand), "):")
    else:
        print("ディーラー ( ?? )")
    flag = True
    for card in dealer_hand:
        if flag or uncovered:
            print("[", card[SUIT], card[RANK], "]")
            flag = False
        else:
            print("[ * * ]")
    print()


# デッキの作成
def make_deck():
    suits = ["S", "H", "D", "C"]  # スートの定義
    ranks = range(1, 14)  # ランクの定義
    deck = [(x, y) for x in ranks for y in suits]
    random.shuffle(deck)  # シャッフルする
    return deck


def main():
    turn = 1
    player_money = 100
    deck = make_deck()  # 山札の再構築

    while player_money > 0:
        print("-" * 20)  # 区切り線を作る
        print("ターン：", turn)
        print("所持金：", player_money)
        print("-" * 20)  # 区切り線を作る

        player_hand = []  # プレイヤーの手札
        dealer_hand = []  # ディーラーの手札
        deck = make_deck()  # デッキの作成

        try:
            bet = int(input("ベット額 > "))
        except:
            print("整数で入力してください")
            continue

        # 入力値が所持金額を超えていたらやり直し
        if bet > player_money:
            print("所持金が不足しています")
            continue
        # 入力値が0より小さかったらやり直し
        elif bet <= 0:
            print("ベットできる額は1以上です")
            continue

        player_money -= bet

        if len(deck) < 10:  # 残り10以下なら再構築
            deck = make_deck()

        # card = deck.pop()  # デッキのリストの末尾の値
        # player_hand.append(card)  # プレイヤー手札に加える
        # card = deck.pop()  # (A)
        # player_hand.append(card)  # プレイヤー手札に加える2枚目
        # card = deck.pop()  # デッキのリストの末尾の値
        # dealer_hand.append(card)  # ディーラー手札に加える
        # card = deck.pop()  # (A)
        # dealer_hand.append(card)  # ディーラー手札に加える2枚目

        for i in range(2):  # 互いに2枚ずつ引く
            player_hand.append(deck.pop())  # デッキからPへ配る
            dealer_hand.append(deck.pop())  # デッキからDへ配る

        print("-" * 20)  # 区切り線を作る
        # print(player_hand)  # Pの手札
        # print(get_point(player_hand))  # Pのポイント
        print_player_hand(player_hand)
        # print(dealer_hand)  # Dの手札
        # print(get_point(dealer_hand))  # Dのポイント
        print_dealer_hand(dealer_hand, False)
        print("-" * 20)  # 区切り線を作る

        # プレイヤーターン
        while True:
            op = input("スタンド:1,ヒット:2,ダブル:3 >")
            doubled, ending = player_op(deck, player_hand, op)
            if doubled:  # ダブルしたときの処理
                player_money -= bet
                bet += bet
            if ending:  # ターン終了の処理
                break

        # ディーラーターン
        dealer_op(deck, player_hand, dealer_hand)

        message, player_money = win_lose(dealer_hand, player_hand, bet, player_money)
        print(message)

        print("-" * 20)  # 区切り線を作る
        print_player_hand(player_hand)
        print_dealer_hand(dealer_hand, True)  # 終了時ディーラー手札を表示
        print("-" * 20)  # 区切り線を作る

        turn += 1
        input("次のターンへ")
    print("ゲームオーバー")


if __name__ == "__main__":
    main()
