from typing import List
from enum import Enum

CARDS = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]
ALT_CARDS = ["J", "2", "3", "4", "5", "6", "7", "8", "9", "T", "Q", "K", "A"]


class Hand(Enum):
    HIGH_CARD = 0
    ONE_PAIR = 1
    TWO_PAIR = 2
    THREE_OF_A_KIND = 3
    FULL_HOUSE = 4
    FOUR_OF_A_KIND = 5
    FIVE_OF_A_KIND = 6


adjustments = {
    Hand.FOUR_OF_A_KIND: [Hand.FIVE_OF_A_KIND],
    Hand.THREE_OF_A_KIND: [Hand.FOUR_OF_A_KIND, Hand.FIVE_OF_A_KIND],
    Hand.TWO_PAIR: [Hand.FULL_HOUSE],
    Hand.ONE_PAIR: [Hand.THREE_OF_A_KIND, Hand.FOUR_OF_A_KIND, Hand.FIVE_OF_A_KIND],
    Hand.HIGH_CARD: [Hand.ONE_PAIR, Hand.THREE_OF_A_KIND, Hand.FOUR_OF_A_KIND, Hand.FIVE_OF_A_KIND]
}


def main():
    file = open("cards.txt", "r")
    lines = file.readlines()
    calc_bets(lines)
    file.close()


def calc_bets(lines: List[str]):
    hands = []
    for line in lines:
        parts = line.split()
        cards = parts[0].strip()
        bet = parts[1].strip()
        hand = define_hand_of_cards(cards)
        adjusted_hand = define_hand_of_cards(cards, True)
        hands.append({"cards": cards, "bet": int(bet), "hand": hand, "adjusted_hand": adjusted_hand})
    reg_hands = sort_hands(hands)
    adjusted_hands = sort_hands(hands, True)
    sum_bets = 0
    adjusted_sum_bets = 0
    for i in range(0, len(hands)):
        sum_bets += (i + 1) * reg_hands[i]["bet"]
        adjusted_sum_bets += (i + 1) * adjusted_hands[i]["bet"]
    print(f"regular  : {sum_bets}")  # 252656917
    print(f"alternate: {adjusted_sum_bets}")  # 253499763


def count_sames(hand, skip_js=False):
    sames, joker_cnt = {}, None
    for card in hand:
        if skip_js and card == "J":
            joker_cnt = 1 if joker_cnt is None else joker_cnt + 1
            continue
        cnt = sames.get(card, None)
        sames[card] = 1 if cnt is None else cnt + 1
    return {card: cnt for card, cnt in sames.items() if cnt > 1}, joker_cnt


def adjust_hand(hand, joker_cnt):
    if hand == Hand.FULL_HOUSE:
        return hand
    if hand == Hand.FIVE_OF_A_KIND or joker_cnt == 5:
        return Hand.FIVE_OF_A_KIND
    else:
        return adjustments[hand][joker_cnt - 1]


def define_hand_of_cards(cards, adjusted=False):
    cnt_cards, joker_cnt = count_sames(cards, adjusted)
    sames = [cnt for card, cnt in cnt_cards.items()]
    if len(sames) == 0:
        hand = Hand.HIGH_CARD
    elif len(sames) == 1:
        of_a_kinds = [Hand.ONE_PAIR, Hand.THREE_OF_A_KIND, Hand.FOUR_OF_A_KIND, Hand.FIVE_OF_A_KIND]
        hand = of_a_kinds[sames[0] - 2]  # Pair is first in list
    # len should only be 2 now
    elif sames[0] == sames[1] == 2:
        hand = Hand.TWO_PAIR
    # last choice full house
    else:
        hand = Hand.FULL_HOUSE
    # adjust if joker
    if adjusted and joker_cnt is not None:
        return adjust_hand(hand, joker_cnt)
    else:
        return hand


def sort_hands(hands: List, adjusted=False):
    cards = CARDS if not adjusted else ALT_CARDS
    return sorted(hands, key=lambda hand: (
        hand["hand"].value if not adjusted else hand["adjusted_hand"].value,
        cards.index(hand["cards"][0]),
        cards.index(hand["cards"][1]),
        cards.index(hand["cards"][2]),
        cards.index(hand["cards"][3]),
        cards.index(hand["cards"][4])
    ))


if __name__ == "__main__":
    main()
