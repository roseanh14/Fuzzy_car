from fuzzy_autonomous_car import evaluate_fis, verbal_description


def print_example_scenarios() -> None:
    examples = [
        (10, -50, 8),   
        (25, -20, 5),   
        (50, 0, 2),     
        (90, 20, 1),    
        (90, 20, 9),    
    ]

    print("Example scenarios (using scikit-fuzzy):")
    for i, (d, v, t) in enumerate(examples, start=1):
        a = evaluate_fis(d, v, t)
        print(
            f"  Scenario {i}: distance={d} m, rel_speed={v} km/h, "
            f"traffic={t} -> accel = {a:.3f} m/s^2 ({verbal_description(a)})"
        )
    print()


def main() -> None:
    print("Fuzzy control of autonomous vehicle acceleration (Mamdani, scikit-fuzzy)")
    print("------------------------------------------------------------------------")
    print("Note: rel_speed = speed_of_vehicle_in_front - our_speed  [km/h]")
    print("  -> negative: we are faster (closing the gap)")
    print("  -> positive: the front vehicle is faster (gap is increasing)")
    print()

    try:
        d = float(input("Enter distance to vehicle/obstacle [m] (0–120): "))
        v = float(input("Enter relative speed rel_speed [km/h] (-100 to 100): "))
        t = float(input("Enter traffic density [0–10]: "))
    except ValueError:
        print("Error: please enter numeric values.")
        return

    a = evaluate_fis(d, v, t)
    print()
    print(f"Recommended acceleration: {a:.3f} m/s^2")
    print(f"Verbal description: {verbal_description(a)}")


if __name__ == "__main__":
    print_example_scenarios()
    main()
