# Sample Output from Your PDF

Based on your sample CWT travel itinerary PDF, the app successfully parsed and created:

## Flights Parsed (3 total)

### Flight 1: LA2696
- **Route**: SCL → LIM (Santiago to Lima)
- **Departure**: March 23, 2026 at 18:30 (Chile time)
- **Arrival**: March 23, 2026 at 20:10 (Peru time)
- **Reservation Code**: MQBJFAC
- **Ticket Number**: 0456330284053

### Flight 2: LA4905
- **Route**: LIM → BOG (Lima to Bogotá)
- **Departure**: March 24, 2026 at 15:55 (Peru time)
- **Arrival**: March 24, 2026 at 19:10 (Colombia time)
- **Reservation Code**: MQBJFAC
- **Ticket Number**: 0456330284053

### Flight 3: LA711
- **Route**: BOG → SCL (Bogotá to Santiago)
- **Departure**: March 26, 2026 at 22:50 (Colombia time)
- **Arrival**: March 27, 2026 at 06:35 (Chile time)
- **Reservation Code**: MQBJFAC
- **Ticket Number**: 0456330284053

## Hotels Parsed (2 total)

### Hotel 1: CASA ANDINA PREMIUM SAN ISIDRO
- **Check-in**: March 23, 2026 at 15:00 (Peru time)
- **Check-out**: March 24, 2026 at 12:00 (Peru time)
- **Confirmation**: 10066SF006058
- **Address**: Las Orquideas 505 527, San Isidro, PE
- **Phone**: 51 1 3916500

### Hotel 2: NH COLLECTION WTC ROYAL
- **Check-in**: March 24, 2026 at 15:00 (Colombia time)
- **Check-out**: March 26, 2026 at 12:00 (Colombia time)
- **Confirmation**: 5596SF007871
- **Address**: Carrera 8a N 9955, World Trade Center, CO
- **Phone**: 57 1 6341734

## Calendar Events Generated (13 total)

For each flight, 3 events were created:

1. **Commute & Airport** (before departure)
   - SCL: 2.5 hours before (16:00 - 18:30)
   - LIM: 3.5 hours before (12:25 - 15:55)
   - BOG: 3.5 hours before (19:20 - 22:50)

2. **Flight** (with 48-hour alarm)
   - LA2696: 18:30 - 20:10
   - LA4905: 15:55 - 19:10
   - LA711: 22:50 - 06:35

3. **Airport & Commute** (after arrival)
   - LIM: 1 hour after (20:10 - 21:40)
   - BOG: 1.5 hours after (19:10 - 20:40)
   - SCL: 1 hour after (06:35 - 07:35)

For each hotel:
- **Hotel Stay** (marked as "free" time)
  - Casa Andina: 15:00 Mar 23 - 12:00 Mar 24
  - NH Collection: 15:00 Mar 24 - 12:00 Mar 26

## Features Demonstrated

✓ Correct timezone handling (Santiago, Lima, Bogotá)
✓ Proper commute durations based on airport
✓ Flight appointments with 48-hour alarms
✓ Hotel appointments marked as "free" time
✓ Flamingo color (11) for flights/commutes
✓ Sage color (6) for hotels
✓ All details in appointment descriptions
✓ No connection handling needed (flights were on different days)

## Import to Google Calendar

The generated file `travel_calendar.ics` can be imported directly into Google Calendar:
1. Open Google Calendar
2. Click Settings (gear icon) → Import & Export
3. Choose the .ics file
4. Select your destination calendar
5. Click Import
