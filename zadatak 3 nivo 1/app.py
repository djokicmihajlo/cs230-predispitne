INCREMENTS = {
    "P1": 5,
    "P2": 6,
    "P3": 2,
}


def local_time(process, global_tick):
    return INCREMENTS[process] * global_tick


def main():
    timeline = [
        ("P1 salje m1 ka P2", "P1", 1, local_time("P1", 1)),
        ("m1 stize na P2", "P2", 2, local_time("P2", 2)),
        ("P2 salje m2 ka P3 posle 1 takta obrade", "P2", 3, local_time("P2", 3)),
        ("m2 stize na P3", "P3", 6, local_time("P3", 6)),
        ("P3 salje odgovor ka P2 posle 1 takta obrade", "P3", 7, local_time("P3", 7)),
        ("odgovor stize na P2", "P2", 10, local_time("P2", 10)),
        ("P2 prosledjuje m4 ka P1 posle 5 taktova", "P2", 15, local_time("P2", 15)),
        ("m4 stize na P1", "P1", 16, local_time("P1", 16)),
    ]

    print("Vremenska linija bez Lamportovog algoritma:")
    for description, process, global_tick, process_time in timeline:
        print(
            f"- globalni takt {global_tick:>2}: {description}; "
            f"{process} vreme = {process_time}"
        )

    p1_time_without_lamport = local_time("P1", 16)
    p2_send_m4_time = local_time("P2", 15)
    p1_receive_m4_time_before_lamport = local_time("P1", 16)
    p1_time_with_lamport = (
        max(p1_receive_m4_time_before_lamport, p2_send_m4_time) + INCREMENTS["P1"]
    )

    print()
    print(f"Bez algoritma: m4 stize na P1 kada P1 pokazuje {p1_time_without_lamport}.")
    print(
        "Sa Lamportovim algoritmom: "
        f"max({p1_receive_m4_time_before_lamport}, {p2_send_m4_time}) "
        f"+ {INCREMENTS['P1']} = {p1_time_with_lamport}."
    )


if __name__ == "__main__":
    main()
