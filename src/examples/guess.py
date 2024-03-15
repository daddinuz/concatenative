from concatenative import MapOrElse, TryMap, Filter, eq, prompt


def guess() -> None:
    return "enter a number: " >> (
        prompt
        | TryMap(int)
        | MapOrElse(
            Filter(eq(42))
            | MapOrElse[int, None](
                lambda _: print("right guess"),
                lambda: print("wrong guess"),
            ),
            lambda: print("invalid number"),
        )
    )


def main() -> None:
    guess()


if __name__ == "__main__":
    main()
