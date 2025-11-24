# Fuzzy Control of Autonomous Vehicle Acceleration (Mamdani FIS)

The goal of this project is to design and implement a Mamdani-type fuzzy inference system that controls the acceleration of an autonomous vehicle based on current traffic conditions.

The system should react to changing conditions in order to keep the ride both smooth and safe. The fuzzy controller uses the following input variables:

- **Distance** to the preceding vehicle or obstacle (0–120 m)  
- **Relative speed** with respect to the preceding vehicle (−100 to 100 km/h)  
- **Traffic density** in the surrounding area (0–10)

The fuzzy system is implemented in **Python** using the libraries **NumPy** and **scikit-fuzzy**.

---

## 1. Fuzzy system design

### 1.1 Input variables and membership functions

All membership functions are simple **triangular** fuzzy sets (triangular membership functions), which keeps the design easy to understand and implement.

#### Distance [m] (0–120)

The distance to the preceding vehicle is described by four fuzzy sets:

- `very_close`: [0, 0, 30]  
- `close`: [10, 30, 60]  
- `medium`: [40, 70, 100]  
- `far`: [80, 120, 120]

This reflects the idea that small distances are critical for safety, while medium and far distances give more flexibility for acceleration.

#### Relative speed [km/h] (−100 to 100)

The relative speed is described by five fuzzy sets:

- `closing_fast`:  [-100, -100, -40]  
- `closing`:       [-80, -40, 0]  
- `stable`:        [-10, 0, 10]  
- `opening`:       [0, 40, 80]  
- `opening_fast`:  [40, 100, 100]

Negative values (closing) indicate that our car is faster and the distance is shrinking. Positive values (opening) mean the front car is faster and the gap is increasing.

#### Traffic density [0–10]

Traffic density is described by three fuzzy sets:

- `low`:    [0, 0, 3]  
- `medium`: [2, 5, 8]  
- `high`:   [7, 10, 10]

Low traffic allows more aggressive acceleration, while high traffic requires more cautious behaviour.

### 1.2 Output variable – acceleration [m/s²] (−5 to 5)

The output acceleration is described by five fuzzy sets:

- `strong_brake`:      [-5, -5, -2.5]  
- `brake`:             [-4, -2, -0.5]  
- `zero`:              [-1, 0, 1]  
- `accelerate`:        [0.5, 2, 4]  
- `strong_accelerate`: [2.5, 5, 5]

These sets represent different levels of braking and acceleration, from strong braking to strong acceleration.

### 1.3 Inference method

The system uses a **Mamdani** fuzzy inference approach with:

- **AND** operator: minimum (`min`)  
- **Aggregation** of rules: maximum (`max`)  
- **Defuzzification**: centroid (center of gravity), implemented internally by `scikit-fuzzy`.

The `scikit-fuzzy` library (`skfuzzy.control`) handles fuzzification, rule evaluation, aggregation, and defuzzification.

---

## 2. Rule base and justification

The rule base is designed around a few main principles:

1. **Safety first** – small distances should lead to braking.  
2. **Traffic-aware behaviour** – in high traffic the system should be more conservative.  
3. **Efficient driving** – if the distance is safe and the front vehicle is pulling away, acceleration is allowed.

### 2.1 Safety rules

If the distance is **very close**, the system always recommends strong braking, regardless of other inputs:

- IF distance is *very_close* AND rel_speed is *closing_fast* THEN accel is *strong_brake*  
- IF distance is *very_close* AND rel_speed is *closing* THEN accel is *strong_brake*  
- IF distance is *very_close* THEN accel is *strong_brake*

These rules guarantee that dangerous situations are handled with maximum braking.

### 2.2 Close distance

When the distance is **close**, the behaviour depends mainly on relative speed and traffic:

- If we are **closing fast** → strong braking  
- If we are closing and traffic is **high** → strong braking  
- If we are closing and traffic is **medium** → mild braking  
- If the speed is **stable** and traffic is **high** → mild braking  
- If the speed is **stable** and traffic is **low** → keep current speed

This ensures safety in heavy traffic and allows neutral behaviour when traffic is light.

### 2.3 Medium distance

For **medium** distance:

- If we are **closing** (fast or slow) → mild braking  
- If speed is **stable** and traffic is **low** → mild acceleration  
- If speed is **stable** and traffic is **medium** → keep speed  
- If the front vehicle is **opening**:
  - with **low** traffic → strong acceleration  
  - with **medium** traffic → mild acceleration  
  - with **high** traffic → keep speed

The system tries to maintain a safe distance but allows acceleration when the front vehicle is pulling away and traffic is not too dense.

### 2.4 Far distance

For **far** distance:

- If the front vehicle is **opening** or **opening_fast** and traffic is **low** → strong acceleration  
- If traffic is **medium** or **high** → mild acceleration

When the distance is large, the system tends to accelerate, but still considers traffic density to avoid unsafe behaviour.

---

## 3. Evaluation of the fuzzy system

The implementation includes five example scenarios, each defined by a combination of:

- distance [m]  
- relative speed [km/h]  
- traffic density [0–10]

The fuzzy system was evaluated for the following scenarios:

| Scenario | Distance [m] | rel_speed [km/h] | Traffic | Acceleration [m/s²] | Description           |
|---------:|-------------:|-----------------:|:--------|---------------------:|-----------------------|
| 1        | 10           | -50              | 8       | -4.097               | strong braking        |
| 2        | 25           | -20              | 5       | -2.481               | mild braking          |
| 3        | 50           | 0                | 2       | 1.429                | mild acceleration     |
| 4        | 90           | 20               | 1       | 3.944                | strong acceleration   |
| 5        | 90           | 20               | 9       | 1.307                | mild acceleration     |

### 3.1 Discussion

- **Scenario 1:**  
  Distance is very small (10 m), we are closing fast (−50 km/h) and traffic is high.  
  The system outputs strong braking (≈ −4.1 m/s²), which is appropriate for safety.

- **Scenario 2:**  
  Distance is 25 m, we are still closing (−20 km/h) and traffic is medium.  
  The system recommends mild braking (≈ −2.48 m/s²), reducing speed to increase the gap.

- **Scenario 3:**  
  Medium distance (50 m), almost the same speed (0 km/h difference) and low traffic.  
  The system suggests mild acceleration (≈ 1.43 m/s²), which is reasonable and keeps the drive efficient.

- **Scenario 4:**  
  Large distance (90 m), the front vehicle is faster (+20 km/h) and traffic is very low.  
  The system outputs strong acceleration (≈ 3.94 m/s²), which helps to close the large gap in free traffic.

- **Scenario 5:**  
  Same kinematics as Scenario 4, but very high traffic density (9).  
  The acceleration is reduced to mild acceleration (≈ 1.31 m/s²), showing that the controller becomes more conservative in heavy traffic.

Overall, the fuzzy controller behaves as expected: it strongly prioritizes safety at small distances and in high traffic, while allowing stronger acceleration when the distance is large and traffic is light.

---

## 4. Installation and usage

### 4.1 Requirements

- **Python 3.10+** (tested with Python 3.12)
- Libraries:
  - `numpy`
  - `scipy`
  - `scikit-fuzzy`
  - `networkx`

### 4.2 Installation on Windows 10 / 11

1. Install Python 3 from the official website (make sure to check *“Add Python to PATH”* during installation).
2. Open **PowerShell**.
3. Install the required libraries:

   ```powershell
   py -m pip install numpy scipy scikit-fuzzy networkx

   Run the application:
     py main.py
