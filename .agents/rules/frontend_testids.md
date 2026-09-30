# Frontend QA Test IDs — Rules

This document establishes the mandatory convention for adding `data-testid` attributes to interactive and stateful elements across the React frontend. Adhering to these rules ensures predictable, robust automation with Model Context Protocol (MCP) browser tools (such as Playwright) and automated test suites.

---

## 1. Core Principle & Philosophy

- **Actionable Elements MUST have a test ID**: Every interactive element (buttons, inputs, links, dropdowns, toggles, checkboxes, scrollers) must provide a test ID.
- **Stateful/Dynamic Data Elements MUST have a test ID**: Every dynamic data element (error messages, success banners, dynamic cards, empty states, loading indicators, rating scores) must provide a test ID.
- **Static Headings & Layout Wrappers MUST NOT have a test ID**: Do NOT add test IDs to static headings (`<h1>`, `<h2>`, page titles) or passive layout containers (`Box`, `Grid`, `Stack`). Keep the DOM test ID footprint clean, concise, and focused.
- **Repeatable & Non-Unique for Collections**: Repeated items in lists, tables, or dynamic forms MUST use **uniform, non-unique test IDs** (e.g., all anime cards have `data-testid="qa-anime_card-card"`, all dynamic season cards have `data-testid="qa-kitsu_season_card-card"`). Never embed unpredictable database IDs or dynamic titles into the test ID. MCP and Playwright select specific items using `.nth(i)`, `.first()`, `.last()`, or `.filter({ hasText: '...' })`.

---

## 2. Slug Specification

Every test ID must follow this exact 3-segment format:

```
qa-<element_name>-<action_or_data>
```

### Segment Breakdown

1. **`qa-`** *(Required prefix)*:
   Identifies the hook as belonging to the QA / test automation layer.

2. **`<element_name>`** *(snake_case identifier)*:
   Descriptive name indicating the component, field, or entity.
   - Forms & static controls: `signin_email`, `signup_submit`, `kitsu_search_input`, `add_anime_submit`
   - Collections & repeated items: `anime_card`, `season_card`, `kitsu_season_card`, `review_card`
   - Inner collection elements: `anime_link`, `kitsu_season_id`, `kitsu_season_remove`, `season_rate_btn`

3. **`<action_or_data>`** *(semantic category)*:
   Categorizes whether the element performs an action or displays dynamic data.

   **Action Categories:**
   | Suffix | Purpose | Examples |
   |---|---|---|
   | `input` | Text, number, email, password, or textarea input | `qa-signin_email-input`, `qa-kitsu_season_id-input` |
   | `click` | Clickable buttons, navigation links, icons | `qa-nav_anime-click`, `qa-kitsu_season_remove-click` |
   | `submit` | Form submission or rating lock/save buttons | `qa-signin_submit-submit`, `qa-rating_lock_btn-submit` |
   | `select` | Dropdown selects and menu options | `qa-anime_type-select`, `qa-kitsu_season_type-select` |
   | `toggle` | Checkboxes, switches, or expandable toggles | `qa-anime_nsfw-toggle`, `qa-kitsu_season_has_parts-toggle` |
   | `drag` | Draggable handles, sliders, scrollers | `qa-rating_slider-drag` |

   **Data & State Categories:**
   | Suffix | Purpose | Examples |
   |---|---|---|
   | `card` | Card representing a dynamic entity in a list | `qa-anime_card-card`, `qa-kitsu_season_card-card`, `qa-review_card-card` |
   | `data` | Dynamic data field (ratings, user names, counts) | `qa-anime_rating-data`, `qa-nav_user_name-data` |
   | `error` | Error alerts and validation messages | `qa-signin_error-error`, `qa-kitsu_single_error-error` |
   | `status` | Success banners and informational notices | `qa-kitsu_single_success-status` |
   | `loading` | Loading spinners, skeletons, or indicators | `qa-anime_list_loading-loading` |
   | `empty` | Empty state indicators | `qa-anime_list_empty-empty`, `qa-community_reviews_empty-empty` |
   | `list` | Container feed or collection list | `qa-community_reviews-list` |

---

## 3. Reusable Form Components Standard

All reusable form components in `src/FormComps/` must:
1. Accept an optional `testId?: string` prop.
2. If `testId` is not provided, automatically derive a compliant test ID from `id` or `label`:
   `qa-${props.id.replace(/[^a-zA-Z0-9]+/g, '_').toLowerCase()}-input` (or `-select`, `-toggle`).
3. For Material-UI `<TextField>` components, pass the test ID into `inputProps={{ 'data-testid': testId }}` so MCP tools and Playwright can target and fill the native `<input>` directly without targeting the wrapper `div`.

```tsx
interface InputProps {
  id: string;
  label: string;
  value: string;
  onChange: (value: string) => void;
  testId?: string;
}

const InputComponent = (props: InputProps): JSX.Element => {
  const derivedTestId = props.testId || `qa-${props.id.replace(/[^a-zA-Z0-9]+/g, '_').toLowerCase()}-input`;

  return (
    <FormControl fullWidth>
      <TextField
        data-testid={derivedTestId}
        inputProps={{ 'data-testid': derivedTestId }}
        id={props.id}
        label={props.label}
        value={props.value}
        onChange={(e) => props.onChange(e.target.value)}
      />
    </FormControl>
  );
};
```

---

## 4. MCP & Playwright Interaction Patterns

Because collection items are uniform and non-unique, write locators using Playwright's built-in filtering and indexing:

```ts
// 1. Count items
await page.locator('[data-testid="qa-anime_card-card"]').count();

// 2. Select first or last item
await page.locator('[data-testid="qa-anime_card-card"]').first().click();

// 3. Select an item by text content
const deathNoteCard = page.locator('[data-testid="qa-anime_card-card"]').filter({ hasText: 'Death Note' });
await deathNoteCard.locator('[data-testid="qa-anime_link-click"]').click();

// 4. Fill dynamically added season rows (e.g. season 2)
const season2Card = page.locator('[data-testid="qa-kitsu_season_card-card"]').nth(1);
await season2Card.locator('[data-testid="qa-kitsu_season_id-input"]').fill('12345');
```
