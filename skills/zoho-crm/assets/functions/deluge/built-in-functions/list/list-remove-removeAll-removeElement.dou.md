FILE_PURPOSE: Deluge `remove()` / `removeAll()` / `removeElement()` — three ways to remove from a LIST.

MENTAL_MODEL: remove(i) removes+returns by index; removeAll(list) and removeElement(val) mutate list in-place.

WHEN_TO_USE:
- Remove element by index and capture it → use remove()
- Bulk-remove all elements present in another list → use removeAll()
- Remove a specific element by value → use removeElement()

WHEN_NOT_TO_USE:
- Need to empty the entire list → use clear()
- Need to remove by index without capturing the element → remove() still works but discards the return value

TRIGGER_KEYWORDS: remove(), removeAll(), removeElement(), list-mutate-removal, index-vs-element-based-removal

RULES:
1. remove(indexValue): removes AND returns the element at the 0-based indexValue. Return type: TEXT. Mutates list.
2. remove(): negative indexValue → runtime error. indexValue >= list size → runtime error.
3. removeAll(removeListVariable): removes all elements in removeListVariable from listVariable. If an element is not found, listVariable is unchanged. No return value (void; mutates in-place).
4. removeElement(searchElement): removes first occurrence of searchElement by value. If not found, list unchanged. No return value (void; mutates in-place).
5. removeElement(): if the list is a typed list and searchElement data type mismatches the list's type → runtime error.

CANONICAL_EXAMPLES:
```deluge
// remove() — by index, returns removed element
Product = {"Leads", "Contacts", "Deals"};
element = Product.remove(1); // element = "Contacts"; Product = {"Leads", "Deals"}

// removeAll() — removes all elements present in the second list
Products = {"Leads", "Contacts", "Deals"};
removeProducts = {"CRM", "Projects"};
Products.removeAll(removeProducts); // Products = {"Leads"}

// removeElement() — by value, first occurrence
Product = {"Leads", "Contacts", "Deals"};
Product.removeElement("Contacts"); // Product = {"Leads", "Deals"}
```

FAILURE_MODES:
- remove() with negative index → runtime error
- remove() with index >= list size → runtime error
- removeElement() with type-mismatched value on a typed list → runtime error
- removeAll() / removeElement() return no value — do NOT assign to a variable expecting a result

RELATED_DOCS:
- clear() — list-get-size-clear.dou.md
- indexOf() — list-indexOf-lastIndexOf.dou.md
- List functions — https://www.zoho.com/deluge/help/functions/list.html

SOURCE:
https://www.zoho.com/deluge/help/functions/list/remove.html, https://www.zoho.com/deluge/help/functions/list/removeall.html, https://www.zoho.com/deluge/help/functions/list/removeelement.html
