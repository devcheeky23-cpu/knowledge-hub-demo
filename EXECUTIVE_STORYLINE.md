# Executive Storyline — Project Knowledge Hub

One-page pitch. Lead with business language; go technical only when asked.

---

## 1. Problem

ความรู้ของโปรเจกต์กระจัดกระจาย — อยู่ใน PRD, API spec, chat, และในหัวคน
ไม่มีศูนย์กลาง

- Developer ถามซ้ำเรื่องเดิม (API รับ-คืน field อะไร, design เป็นยังไง) → เสียเวลาทั้งคนถามและคนตอบ
- ส่งต่อความรู้ตกหล่น: PM/BA/SA → dev, backend → frontend
- คนลาออก = ความรู้หายตามไป
- **ผลกระทบ:** delivery ช้าลง, onboarding คนใหม่นาน, ถาม-ตอบซ้ำกินเวลาทีมทุกสัปดาห์

---

## 2. Value

ศูนย์กลางความรู้ที่ถามด้วยภาษาธรรมชาติ แล้วได้คำตอบจากเอกสารจริง

| ผลลัพธ์ | วัดด้วย |
|---------|---------|
| Dev หาคำตอบเองได้ ไม่ต้องรบกวนคนอื่น | จำนวนคำถามซ้ำที่ลดลง / เวลาที่ประหยัด |
| Onboarding คนใหม่เร็วขึ้น | เวลาจนกว่าจะ productive |
| ความรู้ไม่หายเมื่อคนลาออก | คำถามที่ตอบได้จากเอกสาร |
| ชี้จุดที่เอกสารขาด | gap report (คำถามที่ระบบ abstain) |

---

## 3. Approach + Demo

**หลักการ:** RAG — ระบบดึงคำตอบจากเอกสารบริษัทจริงเท่านั้น พร้อมอ้างอิงที่ตรวจสอบได้ ไม่เดา

**Demo สด — 3 พฤติกรรม:**
1. **Found** — ถาม "Order API รับ field อะไร" → ตอบ + citation คลิกดูต้นฉบับได้
2. **Abstain** — ถามนอกเอกสาร → "ไม่พบข้อมูลในเอกสาร" (ไม่เดา)
3. **Conflict** — เอกสาร 2 ที่ขัดแย้ง → โชว์ทั้งสองฝั่ง + citation ไม่เลือกข้าง

**Data + Boundary:**
- ใช้เฉพาะเอกสารที่ import เข้าระบบ (1 project)
- ตอบจาก context ที่ดึงมาเท่านั้น — ไม่ใช้ความรู้ทั่วไปของโมเดล
- ทุกคำตอบมี citation → ตรวจสอบได้

---

## 4. Risk & Control

| Risk | Control | Owner |
|------|---------|-------|
| Hallucination (ตอบมั่ว) | บังคับตอบจากเอกสาร + บังคับ citation + abstain เมื่อไม่เจอ | Dev team |
| Data leakage (ข้อมูลรั่ว) | MVP ใช้ mock data; production ย้าย paid API/self-host | Data owner |
| Wrong info ใช้งานจริง | ทุกคำตอบมี citation ให้ user ตรวจก่อนใช้ | ผู้ใช้ |
| Access boundary | 1 project; future: per-user access control | Admin |
| Conflict ในเอกสาร | ระบบรายงาน conflict ไม่ตัดสินเอง | ผู้ใช้ตัดสิน |

**หลักการ:** ความเสี่ยงไม่ได้แปลว่าห้ามทำ — แปลว่าต้องมี control ที่เหมาะสม

---

## 5. Implementation Path

**Pilot (2 สัปดาห์):**
- เลือก 1 project, seed เอกสารจริง 5–10 ไฟล์ (ไม่มีข้อมูลลับ)
- เตรียม golden question set 15–20 ข้อจากคำถามที่ dev ถามจริง
- วัดผล: ตอบถูก ≥70–80% + ทุกคำตอบมี citation + abstain ถูกเมื่อไม่มีข้อมูล

**Scale:**
- ย้าย persistent storage + paid/self-hosted model (privacy)
- รองรับหลาย project + per-user access control
- เพิ่ม gap report, code indexing, auto-sync กับ git

---

## Q&A Buffer (เตรียมตอบ ไม่ต้องพูดเอง)

- **ต่างจาก ChatGPT ยังไง?** → ChatGPT เดาได้ ข้อมูลออกนอกองค์กร คุม behavior ไม่ได้; ของเราตอบจากเอกสารเท่านั้น + citation + คุม retrieval/abstain/conflict + deploy ใน infra เองได้
- **Abstain GPT ก็ทำได้?** → ได้ถ้าสั่ง แต่ของเราเป็น default ที่การันตี + วัดผลได้ + คุม retrieval เองได้ (รองรับไทย)
- **ทำไมไม่ใช้ ChatGPT เลย?** → privacy + คุม retrieval (ภาษาไทย) + conflict mode + integrate เข้า workflow ได้
